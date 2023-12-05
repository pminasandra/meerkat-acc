# Pranav Minasandra
# pminasandra.github.io
# 04 Dec, 2023

"""
Adds a percentile-function-applied VeDBA column to all available feature data
"""

import glob
import os.path

import pandas as pd

import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint


def add_perc_col(df):
    """
    Adds a percentile-VeDBA column to the given feature df
    df (pd.DataFrame): a loaded features csv
    inplace (bool): whether to edit the col in place
    """

    df_c = df.copy()
    df_c['perc_vedba'] = df_c['mean_vedba'].rank()/len(df_c['mean_vedba'])

    return df_c


def add_cols_to_all_files():
    """
    Adds perc_vedba columns to all available feature files
    """

    feature_files = glob.glob(os.path.join(config.DATA, "Features",
                                            "*/*_extracted_features.csv"))
    for file_ in feature_files:
        print(file_)
        df = pd.read_csv(file_)
        df = add_perc_col(df)
        df.to_csv(file_, index=False)

if __name__ == "__main__":
    add_cols_to_all_files()
