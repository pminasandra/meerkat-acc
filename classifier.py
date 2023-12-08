# Pranav Minasandra
# pminasandra.github.io
# Nov 30, 2023

"""
Implement random forest classifier
"""

import glob
import os.path

import pandas as pd
import sklearn.ensemble

import auditreading
import config
import extractor
import utilities

ALL_FEATURES = list(extractor.ALL_FEATURES.keys())
ALL_FEATURES.append('perc_vedba')

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
        return pd.DataFrame()

    all_data = [pd.read_csv(file_) for file_ in tgtfiles]
    all_data = pd.concat(all_data)
    all_data['Timestamp'] = pd.to_datetime(all_data['Timestamp'])

    all_data.sort_values(by='Timestamp', inplace=True)
    all_data.reset_index(inplace=True)

    return all_data


def load_all_training_data():
    """
    Loads all available feature and audit data to RAM.
    Returns: pd.DataFrame
    """

    all_training_data = []

    for dplment in config.DEPLOYMENTS:
        for individual in config.INDIVIDUALS[dplment]:
            ft_data = load_feature_data_for(dplment, individual)
            audit_data = auditreading.load_audit_data_for(dplment, individual)

            cols_needed = list(ft_data.columns)
            cols_needed.append("Behavior")
            cols_needed.remove('index')
# so much fighting pandas happening at this stage
# just wanna switch to c++ or something lmao
            training_data = ft_data.join(audit_data.set_index('Timestamp'),
                                    on='Timestamp',
                                    how='inner',
                                    lsuffix="_l",
                                    rsuffix="_r"
                                    )

            del ft_data
            del audit_data

            training_data = training_data[cols_needed]
            training_data.sort_values(by='Timestamp')
            training_data.reset_index(inplace=True)

            training_data['Deployment'] = dplment
            training_data['Individual'] = individual

            all_training_data.append(training_data)

    all_training_data = pd.concat(all_training_data)
    all_training_data.reset_index(inplace=True)
    return all_training_data


def train_random_forest(train_features, train_classes):
    """
    Creates and trains a random forest classifier.
    Args:
        train_features (list, np.ndarray, or pd.DataFrame)
        train_classes (list, np.ndarray, or pd.DataFrame)
    Returns:
        sklearn.ensemble.RandomForestClassifier
    """
    rfc = sklearn.ensemble.RandomForestClassifier(
            class_weight="balanced"
            )
    rfc.fit(train_features, train_classes)
    return rfc


if __name__=="__main__":
    data = load_all_training_data()
    data = data[["Timestamp", "Deployment", "Individual"]
                    + ALL_FEATURES + ["Behavior"]]
    data.to_csv(os.path.join(config.DATA,
            "ClassifierRelated",
            "all_trainable_data_for_classifier.csv"),
        index=False) 
