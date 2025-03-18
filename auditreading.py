# Pranav Minasandra
# pminasandra.github.io
# Nov 28, 2023
# Yay, happy birthday to me!

"""
Reads and validates behavioral audits.
"""

import datetime as dt
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
    Checks column labels and behavioral states in a given dataframe,
    and performs other fixes.
    """
    assert list(df.columns) == ['Timestamp', 'Behavior'] #labels as chosen by Amlan
    for state in df['Behavior'].unique():
        assert state in config.BEHAVIORS

    # there seems to be a weird
    # offset in Amlan's labelling.
    df["Timestamp"] += dt.timedelta(seconds=config.AMLAN_OFFSET)


def load_auditfile(filepath):
    csvfilepath = filepath
    csvfile = pd.read_csv(csvfilepath)
    csvfile['Timestamp'] = pd.to_datetime(csvfile['Timestamp'])
    validate_audit(csvfile)
    if config.DROP_MISSING:
        csvfile = csvfile[csvfile['Behavior'] != "No observation"]
    if config.COMBINE_BEHAVIORS:
        csvfile['Behavior'] = csvfile['Behavior'].map(
                config.BEHAVIOR_SIMPLIFIER
                )
    if config.DROP_OTHERS:
        csvfile = csvfile[csvfile["Behavior"] != "Others"]

    return csvfile


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
            csvfile = load_auditfile(csvfilepath)
            yield dplment, os.path.basename(csvfilepath)[:-len(".csv")], csvfile


def load_audit_data_for(dplment, individual):
    """
    Loads all available audit data for specified individual from specified 
    deployment.
    Args:
        dplment (str)
        individual (str)
    Returns:
        pd.DataFrame
    Raises:
        AssertionError: when looking for incorrect deployments or individuals.
    """

    assert dplment in config.DEPLOYMENTS
    assert individual in config.INDIVIDUALS[dplment]

    tgtdirpath = os.path.join(config.AUDIT_DIR, dplment)
    tgtfiles = glob.glob(os.path.join(tgtdirpath, f"*{individual}*.csv"))

    if len(tgtfiles) == 0:
        return pd.DataFrame({"Timestamp": [], "Behavior": []})

    all_data = [pd.read_csv(file_) for file_ in tgtfiles]
    all_data = pd.concat(all_data)
    all_data['Timestamp'] = pd.to_datetime(all_data['Timestamp'])
    validate_audit(all_data)

    all_data.sort_values(by='Timestamp', inplace=True)
    all_data.reset_index(inplace=True)

    if config.DROP_MISSING:
        all_data = all_data[all_data['Behavior'] != "No observation"]
    if config.COMBINE_BEHAVIORS:
        all_data['Behavior'] = all_data['Behavior'].map(config.BEHAVIOR_SIMPLIFIER)
    if config.DROP_OTHERS:
        all_data = all_data[all_data["Behavior"] != "Others"]

    return all_data


if __name__ == "__main__":
    auditgen = load_audits()
    for dplment, name, df in auditgen:
        print("\n", dplment, name, "\n", df)
