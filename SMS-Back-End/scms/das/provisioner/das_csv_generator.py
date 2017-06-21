# -*- coding: utf-8 -*-

"""
Program to generate file of n lines of random values to try tools to data analysis,
like an approach to the real scenario.

Example:

    python das_csv_generator.py  --generator attendances
    python das_csv_generator.py  --generator marks
"""

import argparse
import csv
import datetime
from datetime import timedelta
from random import randint
import random

parser = argparse.ArgumentParser(description='Tool to generate csv files to try data analysis tools.')
parser.add_argument('--generator', help='Generator used')
args = parser.parse_args()


# General params:

days = 180 # +- 9 months
students_per_class = 30
subjects = 8
classes = 2


def attendance_controls_generator(file):

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
                for student_num in range(1, students_per_class+1):

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


def marks_generator(file):

    # We write the description of generator schema:
    item = ['markId',
            'studentId', 'enrollmentId',
            'preFirstEv', 'firstEv',
            'preSecondEv', 'secondEv',
            'thirdEv',
            'final',
            ]

    def normalize(mark):
        if mark < 0.0: return 0.0
        if mark > 10.0: return 10.0
        if mark >= 0.0 and mark <= 10.0: return mark

    def own_random(a, b):
        return round(random.uniform(2, -4.5), 1)

    file.writerow(item)

    mark_num = 0;
    for class_num in range(classes):
        for subject_num in range(subjects):
            for student_num in range(students_per_class):

                preFirstEv = random.uniform(0,10)
                # In 75% of cases firstEv mark is 2 points plus of preFirstEv exam mark.
                if random.uniform(0, 100) <= 75:
                    mark = preFirstEv + 2;
                # In the rest of cases the variation is only 1 point.
                else:
                    mark = preFirstEv + random.uniform(-1, 1)
                firstEv = normalize(mark)


                # In the 75% of cases the mark of preSecondEv decrement in 1 point
                if random.uniform(0, 100) <= 75:
                    mark = firstEv - 1;
                # In the rest of cases the variation is only 1.5 points.
                else:
                    mark = firstEv + random.uniform(-1.5, 1.5)
                preSecondEv = normalize(mark)
                # In 90% of cases secondEv mark is 1 points plus of preSecondEv exam mark.
                if random.uniform(0, 100) <= 90:
                    mark = preFirstEv + 1;
                # In the rest of cases the variation is only 1 point.
                else:
                    mark = preFirstEv + random.uniform(-1, 1)
                secondEv= normalize(mark)

                # In the 75% of cases the mark of thirdEv decrement in 4 point
                if random.uniform(0, 100) <= 75:
                    mark = secondEv - 4;
                    # In the rest of cases the variation is only 1.5 points.
                else:
                    mark = firstEv + random.uniform(-1.5, 1.5)
                thirdEv = normalize(mark)

                # To the final mark is the average ot three marks and a bit of variation over teacher opinion.
                final = (firstEv+secondEv+thirdEv)/3
                if random.uniform(0, 100) <= 80:
                    final += 0.5;
                # In the rest of cases the variation is only 1 points.
                else:
                    final += random.uniform(1, 1)

                final = normalize(final)

                # Setting the record
                record = [mark_num, student_num, None,
                          round(preFirstEv,1), round(firstEv,1),
                          round(preSecondEv,1), round(secondEv,1),
                          round(thirdEv,1),
                          round(final,1)]
                mark_num +=1

                # Saving the record
                file.writerow(record)


def disciplinary_notes_generator(file):
    pass

if __name__ == "__main__":

    with open('{}.csv'.format(args.generator), 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';')

        if args.generator == 'attendances':
            attendance_controls_generator(spamwriter)

        if args.generator == 'marks':
            marks_generator(spamwriter)

        if args.generator == 'disciplinaryNotes':
            disciplinary_notes_generator(spamwriter)



