# Pranav Minasandra
# pminasandra.github.io
# Nov 30, 2023

"""
Implement random forest classifier
"""

import glob
import os.path

import pandas as pd

import auditreading
import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint


def load_feature_data_for(dplment, individual):
    """
    Loads all available feature data for given deployment and individual.
    Args:
        dplment (str)
        individual (str)
    Returns:
        pd.DataFrame
    Raises:
        AssertionError
    """
    
    assert dplment in config.DEPLOYMENTS
    assert individual in config.INDIVIDUALS[dplment]

    tgtdirpath = os.path.join(config.DATA, "Features", dplment)
    tgtfiles = glob.glob(os.path.join(tgtdirpath, f"*{individual}*.csv"))
    if len(tgtfiles) == 0:
        return pd.DataFrame({
            "Timestamp": [],
            "xmean": [],
            "ymean": [],
            "zmean": [],
            "xvar": [],
            "yvar": [],
            "zvar": [],
            "xmin": [],
            "ymin": [],
            "zmin": [],
            "xmax": [],
            "ymax": [],
            "zmax": [],
            "mean_vedba": []
            })

    all_data = [pd.read_csv(file_) for file_ in tgtfiles]
    all_data = pd.concat(all_data)
    all_data['Timestamp'] = pd.to_datetime(all_data['Timestamp'])

    all_data.sort_values(by='Timestamp', inplace=True)
    all_data.reset_index(inplace=True)

    return all_data


def load_all_training_data():
    """
    Loads all available feature and audit data to RAM.
    Returns: all_data (dict)
        such that: all_data[<dplment>] is a dict
            such that: all_data[<dplment>][<individual>} is a pd.DataFrame.
    """

    ALL_TRAINING_DATA = {}
    for dplment in config.DEPLOYMENTS:
        ALL_TRAINING_DATA[dplment] = {}

    for dplment in config.DEPLOYMENTS:
        for individual in config.INDIVIDUALS[dplment]:
            ft_data = load_feature_data_for(dplment, individual)
            audit_data = auditreading.load_audit_data_for(dplment, individual)

            cols_needed = list(ft_data.columns)
            cols_needed.append("Behavior")
            cols_needed.remove('index')
# so much fighting pandas happening at this stage
# just wanna switch to c++ or something lmao
            training_data = ft_data.join(audit_data.set_index('Timestamp'), on='Timestamp', how='inner', lsuffix="_l", rsuffix="_r")

            del ft_data
            del audit_data

            training_data = training_data[cols_needed]
            training_data.sort_values(by='Timestamp')
            training_data.reset_index(inplace=True)

            ALL_TRAINING_DATA[dplment][individual] = training_data

    return ALL_TRAINING_DATA

if __name__=="__main__":
    data = load_all_training_data()
    print(data)
