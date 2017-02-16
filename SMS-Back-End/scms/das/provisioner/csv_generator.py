# -*- coding: utf-8 -*-

"""
Program to generate file of n lines of random values to try tools to data analysis,
like an approach to the real scenario.

Example:

    python csv_generator.py --filename hola --generator 1


"""

import argparse
import csv
import datetime
from datetime import timedelta
from random import randint

parser = argparse.ArgumentParser(description='Tool to generate csv files to try data analysis tools.')

parser.add_argument('--filename', help='Name of the output file')
parser.add_argument('--lines', help='Number of lines to generate')
parser.add_argument('--generator', help='Generator used')
args = parser.parse_args()





def generator1(file, lines=None):

    days = 60
    students_per_clase = 30
    subjects = 8
    classes = 2

    # Total of lines: 30 students per 2 classes = 60 per 8 subjects = 480 items per 60 days = 28.800 records

    # We write the description of generator schema:
    item = ['studentId', 'classId', 'subjectId', 'teacherId',
            'recordDate', 'recordHour', 'recordWeekday',  'studentAge', 'assistance',
            'delay', 'justifiedDelay', 'uniform']

    file.writerow(item)

    date = datetime.datetime(2000, 1, 3, 8, 0)  # Monday, 3 of January, 2000 8:00

    for day_num in range(days):

        # To avoid weekends to save the date
        if date.weekday() == 5:
            date = date + timedelta(days=2)

        dateFormat = '{}-{}-{}'.format(date.day, date.month, date.year)


        times = [0,5,10,20,30]


        for class_num in range(1, classes+1):
            for subject_num in range(1, subjects+1):
                for student_num in range(1, students_per_clase+1):

                    #We are going to comple a bit more the random generator
                    asistencia = None
                    if randint(0, 100) <= 60:
                        asistencia = 1
                    else:
                        asistencia = 0

                    if asistencia == 1:
                        retraso = times[randint(0,4)]
                        if retraso != 0:
                            retraso_justificado = randint(0,1)

                        uniforme = randint(0,1)
                    else:
                        retraso = 'NULL'
                        retraso_justificado = 'NULL'
                        uniforme = 'NULL'

                    # Because each subject is imparted for each teacher we will use the same number
                    record = [student_num, class_num, subject_num, subject_num,
                              date.date(), date.time().strftime('%H:%M'), date.weekday(), student_num+10, asistencia, retraso, retraso_justificado, uniforme]

                    # Saving the record
                    file.writerow(record)

                # Increment a houre
                date = date + timedelta(hours=1)

            date = date.replace(hour=0, minute=0)

        # Adding day to date.
        date = date + timedelta(days=1)



if int(args.generator) == 1:
    with open('{}.csv'.format(args.filename), 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')

        generator1(spamwriter)



