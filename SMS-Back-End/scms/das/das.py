############################
#   Data Analysis System   #
############################

#import numpy as np
#import pandas as pd



"""
import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../scm/')
from termcolor import colored

from scm import scm_datastore_models as models


def get_general_attendance_report():

    query = models.Record.query()
    items = []

    for result in query.iter():
        items.append(result.to_dict())


    # Convert the list of dict in a pandas dataframe.
    data_frame = pd.DataFrame(items)
    # We extract the result of group like Series object.
    data_frame.groupby(['recordWeekday', 'assistance']).size()


    print items
    return {'status': 1, 'data': items, 'log': None}

"""