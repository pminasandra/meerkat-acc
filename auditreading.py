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

def expand_behaviour_intervals(df):
    """
    Expands behavior events into second-by-second labeled intervals.

    Parameters:
    df (pd.DataFrame): DataFrame with columns ['Time', 'Behavior', 'Behavior type', 'Comment']

    Returns:
    pd.DataFrame: Expanded DataFrame with columns ['datetime', 'behavior', 'comment']
    """
    # Extract all UTC reference timestamps
    timestamp_rows = df[df['Behavior'] == 'Timestamp']
    if timestamp_rows.empty:
        raise ValueError("No Timestamp row found in the data.")

    # Compute estimated video start time by averaging all timestamps
    offsets = timestamp_rows['Time'].values
    utc_times = [dt.datetime.strptime(ts, "%Y-%m-%d %H:%M:%S") for ts in timestamp_rows['Comment']]
    estimated_start_time = sum([(utc - dt.timedelta(seconds=offset)) for utc, offset in zip(utc_times, offsets)], dt.timedelta()) / len(utc_times)

    # Track active behaviors
    active_behaviors = {}
    expanded_rows = []

    for _, row in df.iterrows():
        current_time = estimated_start_time + dt.timedelta(seconds=row['Time'])
        behavior, btype, comment = row['Behavior'], row['Behavior type'], row['Comment']

        if btype == 'START':
            if behavior in active_behaviors:
                print(f"Warning: Overlapping behavior '{behavior}' at {current_time}")
            active_behaviors[behavior] = current_time

        elif btype == 'STOP':
            if behavior not in active_behaviors:
                print(f"Warning: STOP found for '{behavior}' at {current_time} without a START")
                continue
            start_time = active_behaviors.pop(behavior)

            # Fill each second within the behavior duration
            for sec in range(int(start_time.timestamp()), int(current_time.timestamp()) + 1):
                expanded_rows.append({
                    'datetime': dt.datetime.utcfromtimestamp(sec),
                    'behavior': behavior,
                    'comment': comment
                })

    return pd.DataFrame(expanded_rows)


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
