# Pranav Minasandra
# pminasandra.github.io
# Nov 29, 2023

"""
Extract features from ACC data
"""

import os.path

import pandas as pd

import accreading
import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint


ALL_FEATURES = []
def feature(f):
    """
    DECORATOR!!
    Adds functions to a global list.
    Function f must run on a pandas frame view with
    columns ['Timestamp', 'X', 'Y', 'Z'] and must return
    a float.
    """
    ALL_FEATURES.append(f)
    return f


def each_second_of_data(acc_df):
    """
    GENERATOR!!
    """

    accreading.validate_acc_file(acc_df)

    acc_df['TimestampRounded'] = acc_df['Timestamp'].dt.round('1s')
    for time, frame in acc_df.groupby("TimestampRounded"):
        print(time, "\n", frame, sep="")

if __name__ == "__main__":
    accfilegen = accreading.load_acc_files()
    for dplment, filename, df in accfilegen:
        each_second_of_data(df)
