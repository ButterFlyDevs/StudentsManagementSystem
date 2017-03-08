"""
This program simulate the normal work of das program without DataStore,
based on csv file.
"""

import numpy as np
import pandas as pd


def get_general_attendance_report():

    # Read the csv, type of d is: pandas.core.frame.DataFrame
    d = pd.read_csv('provisioner/attendances.csv',sep=';')

    # To get the count of day of the week and count the assistance value:
    # The kind of this return is : pandas.core.series.Series
    recordWeekdayCount = d.groupby(['recordWeekday', 'assistance']).size()

    return recordWeekdayCount


def get_students_attendance_report():

    data_frame = pd.read_csv('provisioner/attendances.csv', sep=';')
    serie = data_frame.groupby(['studentId','assistance']).size()

    return serie

if __name__ == "__main__":

    print (get_general_attendance_report())
    print (get_students_attendance_report())