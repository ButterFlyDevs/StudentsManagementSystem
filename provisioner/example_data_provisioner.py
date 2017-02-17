# -*- coding: utf-8 -*-
"""Data Provisioned Tool.

Tool to insert data with sense in the system to check the way of work of this,
very helpfully in the developing process.

Example:

    > python example_data_provisioner.py

"""

import os
import requests
from termcolor import colored
from faker import Factory
import logging
from random import randint
import progressbar
import argparse

fake = Factory.create('es_ES')  # Set the language from the data in spanish.

logging.basicConfig(filename='provisioner.log', filemode='w', level=logging.INFO)
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
            # I avoided the repeated pairs.
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
    print colored('This script uses Api Gateway microService to save data in the system.', 'red')

    # Reset database!
    os.system("mysql -u root -p\'root\' < SMS-Back-End/dbms/dbapi/DBCreator.sql >/dev/null 2>&1")
    # >/dev/null 2>&1 to avoid warnings in console log.

    num_teachers = 16
    num_students = 80

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

    # Now we need a random array between teachersIds and subjects_classes_associations
    teachers_s_c_associations = random_relations_generator(range(1, num_teachers+1), range(1, len(subjects_classes_association)+1))
    for item in teachers_s_c_associations:
        elements.append({"kind": "impart", "data": {"teacherId": item[0], "associationId": item[1]}})

    elements.append('space')

    # Now we need a random array between studentsIds and subjects_classes_associations
    students_s_c_associations = random_relations_generator(range(1, num_students+1), range(1, len(subjects_classes_association)+1))


    for item in students_s_c_associations:
        elements.append({"kind": "enrollment", "data": {"studentID": item[0], "associationId": item[1]}})




    # Proccess to save data in the database:

    url = url_base + '/entities'
    success = True

    print 'Saving {} elements.'.format(len(elements))
    print '\t {} classes, {} subjects, {} teachers and {} students.'.format(len(classes), len(subjects), num_teachers, num_students)
    print '\t {} subject-class relations, {} imparts relations and {} enrollments relations.'\
        .format(len(subjects_classes_association), len(teachers_s_c_associations), len(students_s_c_associations))
    print 'Please, be patient.'

    bar = progressbar.ProgressBar(maxval=len(elements), \
                                  widgets=[progressbar.Timer(),progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
    i = 0;
    bar.start()

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

        bar.update(i + 1)
        i=i+1

    bar.finish()

    if success:
        print colored('\nDone provision with SUCCESS!', 'green')
        print 'Remember that you can see the data saved in provisioner/provisioner.log file.'

    else:
        print colored('\nProvision FAIL!', 'red')
        print '### There seems to be something wrong, please revise provisioner/provisioner.log to debug. ###'

def provision_scms_simple():

    print colored('### Provisioning example data to SCmS. ###', 'red')
    """
    import requests
    import json
    with open('../SMS-Back-End/scms/test/ADB_example_1.json') as json_data:
        d = json.load(json_data)
        response = requests.post(url='localhost:8003/association', json=d)
    print response
    """


    a = os.system("curl -i -H \"Content-Type: application/json\" -X POST -d @../SMS-Back-End/scms/test/ADB_example_1.json localhost:8003/association")
    b = os.system("curl -i -H \"Content-Type: application/json\" -X POST -d @../SMS-Back-End/scms/test/AC_example_1.json localhost:8003/ac")



def main():
    parser = argparse.ArgumentParser(description='Insert data in the system.')
    parser.add_argument('-ms', type=str, help = 'The microservice selected')
    args = parser.parse_args()

    if args.ms == 'scms':
        provision_scms_simple()

if __name__ == "__main__":
    main()
