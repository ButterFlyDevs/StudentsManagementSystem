# -*- coding: utf-8 -*-

import os
import requests
from termcolor import colored
from faker import Factory
import logging
from random import randint

fake = Factory.create('es_ES')

logging.basicConfig(filename='provisioner/provisioner.log', filemode='w', level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

url_base = 'http://localhost:8001'


def random_relations_generator(group_a, group_b):

    max_num_relations = len(group_a) * len(group_b)
    relations_created = []
    num_relations = randint(1, max_num_relations)

    for relation in range(num_relations):
        # To avoid repeated items.
        while True:
            tmp_relation = [group_a[randint(0, len(group_a)-1)], group_b[randint(0, len(group_b)-1)]]
            if tmp_relation not in relations_created:
                relations_created.append(tmp_relation)
                break

    return relations_created


def test():

    groupA = [1,2]
    groupB = [4,2,1]

    print random_relations_generator(groupA, groupB)
    print len(random_relations_generator(range(1,8+1), range(1,8+1)))


def run():
    print colored('### Provisioning example data to system randomly. ###', 'red')
    print colored('This script uses apigms to save data in the system.', 'red')

    # Reset database!
    os.system('mysql -u root -p\'root\' < SMS-Back-End/dbms/dbapi/DBCreator.sql')

    num_teachers = 16;
    num_students = 80;

    # 8 subjects
    subjects = ['Matemáticas',
                'Lengua',
                'Inglés',
                'Sociales',
                'Literatura',
                'Música',
                'Francés',
                'Dibujo Técnico'
                ]

    # 8 classes
    courses = [1, 2]
    levels = ['ESO', 'Bachillerato']
    words = ['A', 'B']

    classes = []
    for course in courses:
        for level in levels:
            for word in words:
                classes.append({'course': course, 'level': level, 'word': word})

    # List with all elements.
    elements = []

    # Teachers
    for a in range(num_teachers):
        elements.append({"kind": "teacher",
                         "data": {
                             "name": fake.first_name(),
                             "address": fake.last_name() + ' ' + fake.last_name(),
                             "phone": fake.phone_number(),
                             "address": fake.address()
                         }})

    elements.append('space')

    # Students
    for a in range(num_students):
        elements.append({"kind": "student",
                         "data": {
                             "name": fake.first_name(),
                             "address": fake.last_name() + ' ' + fake.last_name(),
                             "phone": fake.phone_number(),
                             "address": fake.address()
                         }})

    elements.append('space')

    # Subjects
    for subject in subjects:
        elements.append({"kind": "subject", "data": {'name':subject}})

    elements.append('space')

    # Classes
    for item in classes:
        elements.append({"kind": "class", "data": {
            "course": item.get('course'),
            "level": item.get('level'),
            "word": item.get('word')
                         }})

    elements.append('space')

    # 8 Subjects and 8 Classes
    # We generate randomly the associations between classes and subjects.
    subjects_classes_association = random_relations_generator(range(1,8+1), range(1,8+1))
    for item in subjects_classes_association:
        elements.append({"kind": "association", "data": {"subjectId": item[0], "classId": item[1]}})

    elements.append('space')

    # Now we need an random array between teachersIds and subjects_classes_associations
    teachers_s_c_associations = random_relations_generator(range(1, num_teachers+1), range(1, len(subjects_classes_association)+1))
    for item in teachers_s_c_associations:
        elements.append({"kind": "impart", "data": {"teacherId": item[0], "associationId": item[1]}})


    url = url_base + '/entities'

    success = True
    # Way to insert the data in the database:
    for element in elements:

        if element is 'space':
            logging.info('\n\n')

        else:
            response = requests.post(url + '/' + element['kind'], json={'data': element['data']})
            if response.status_code != 200:
                success = False
            else:
                response_data = response.json()
                logging.info(str(' ' + element['kind']) + ' ' +
                             str(response_data.get(element['kind']+'Id', None)) +
                             '  ' + str(response_data))

    if success:
        print colored('Done provision with SUCCESS !', 'green')
        print colored('Remember that you can see the data saved in provisioner.log log file.', 'green')

