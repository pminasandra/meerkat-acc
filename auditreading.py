# Pranav Minasandra
# pminasandra.github.io
# Nov 28, 2023
# Yay, happy birthday to me!

import glob
import os.path

import pandas as pd

import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

def validate_audit(df):
    """
    Checks column labels and behavioral states in a given dataframe
    """
    assert list(df.columns) == ['Timestamp', 'Behavior'] #labels as chosen by Amlan
    for state in df['Behavior'].unique():
        assert state in config.BEHAVIORS

def load_audits(list_of_dplments=config.DEPLOYMENTS):
    """
    GENERATOR!!
    Loads and validates dataframes from audit csvs.
    Args:
        list_of_dplments: which deployments to load
    Yields:
        3-tuple: dplment (str), auditname (str), and csvfile (pd.DataFrame)
    Raises:
        AssertionError: if there are inappropriate csvfiles
    """
    for dplment in list_of_dplments:
        tgtpath = os.path.join(config.AUDIT_DIR, dplment)
        for csvfilepath in glob.glob(os.path.join(tgtpath, "*.csv")):
            csvfile = pd.read_csv(csvfilepath)
            validate_audit(csvfile)
            csvfile['Timestamp'] = pd.to_datetime(csvfile['Timestamp'])

            yield dplment, os.path.basename(csvfilepath)[:-len(".csv")], csvfile


if __name__ == "__main__":
    auditgen = load_audits()
    for dplment, name, df in auditgen:
        print("\n", dplment, name, "\n", df)
