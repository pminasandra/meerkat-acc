# Pranav Minasandra
# pminasandra.github.io
# 0 Dec, 2023

"""
Runs all analyses needed sequentially.
"""

import glob
import os
import os.path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import sklearn.metrics
import sklearn.model_selection
from sklearn.preprocessing import StandardScaler

import analyses
import accreading
import config
import classifier
import extractor
import percentiler
import postprocessing
import preprocessing
import utilities

ALL_FEATURES = [f for f in extractor.ALL_FEATURES.keys()]
ALL_FEATURES.append('perc_vedba')

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

if __name__ == "__main__":
# 0. PRE-PROCESSING
#    preprocessing.exterminate_extraneous_column() # already done, don't re-do


# 1. FEATURE EXTRACTION
    extractor.make_features_dir()

    accfilegen = accreading.load_acc_files()
    extractor.extract_all_features(accfilegen)


# 2. ADD perc_vedba COLUMN
    percentiler.add_cols_to_all_files()


# 3. TRAINING DATA PREPARATION
    data = classifier.load_all_training_data()
    data = data[["Timestamp", "Deployment", "Individual"]
                    + ALL_FEATURES + ["Behavior"]]
    data.to_csv(os.path.join(config.DATA,
            "ClassifierRelated",
            "all_trainable_data_for_classifier.csv"),
        index=False)


# 4. CLASSIFIER ANALYSES
    datasource = os.path.join(config.DATA, "ClassifierRelated",
                        "all_trainable_data_for_classifier.csv")
    data = pd.read_csv(datasource)
    if config.LOG_TRANSFORM_VEDBA:
        data['mean_vedba'] += 1e-10
        data['mean_vedba'] = np.log(data['mean_vedba'])

    data_features, data_classes = analyses._split_features_and_classes(data)

    train_features, test_features, train_classes, test_classes =\
        sklearn.model_selection.train_test_split(data_features, data_classes,
        test_size=0.25)

    if config.SCALE_DATA:
        scaler = StandardScaler()
        scaler.fit(train_features)

        train_features = scaler.transform(train_features)
        test_features = scaler.transform(test_features)

    rfc = classifier.train_random_forest(train_features, train_classes)

    fig, ax = plt.subplots()
    analyses.trad_analyze_random_forest(rfc, test_features, test_classes,
                                            fig, ax)
    plt.cla()

    fig, ax = plt.subplots()
    analyses.indwise_analyze_random_forest(data, fig, ax)


# 5. CLASSIFY ALL AVAILABLE TOTAL 
    rfc_total = classifier.train_random_forest(data_features, data_classes)
    classify_all_available_data(rfc_total)


# 6. POST PROCESSING
    postprocessing.pool_individualwise_predictions()

else:
    raise ImportError("the module main.py is not meant for imports")
