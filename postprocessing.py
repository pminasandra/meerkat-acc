# Pranav Minasandra
# pminasandra.github.io
# 04 Dec, 2023

"""
Final clean-up and pooling operations.
NOTE: only to be run after full classification is performed.
"""

import glob
import os
import os.path

import pandas as pd

import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

FINAL_PREDICTIONS_DESTINATION = os.path.join(config.DATA,
                                    "PredictionsByIndividual_VeDBA")
DEPLOYMENTWISE_INDIVIDUAL_FILES_DEST = os.path.join(config.DATA,
                                    "PredictionsByIndividualDeploymentwise_VeDBA")

def pool_individualwise_predictions():
    """
    Joins all available predictions together by individual.
    """

    os.makedirs(FINAL_PREDICTIONS_DESTINATION, exist_ok=True)

    all_files = glob.glob(os.path.join(
                                config.DATA,
                                "Predictions_VeDBA",#where file-wise predictions are.
                                "*",
                                "*_predictions.csv"
                            )
                        )

    unique_inds = [os.path.basename(f).split('_')[1] for f in all_files]
    for ind in unique_inds:
        ind_preds = []
        ind_files = [f for f in all_files if ind in f]

        for file_ in ind_files:
            df = pd.read_csv(file_)
            df['datetime'] = pd.to_datetime(df['datetime'])
            ind_preds.append(df)

        ind_preds = pd.concat(ind_preds)
        ind_preds.sort_values(by="datetime", inplace=True)
        #ind_preds.reset_index(inplace=True)

        ind_preds.to_csv(os.path.join(FINAL_PREDICTIONS_DESTINATION, 
                                        ind + ".csv"),
                        index=False)

def pool_deploymentwise_predictions():
    """
    Pools predictions by individuals together, but preserves deployments
    """
    os.makedirs(DEPLOYMENTWISE_INDIVIDUAL_FILES_DEST, exist_ok=True)

    for dplment in config.DEPLOYMENTS:
        all_files = glob.glob(os.path.join(
                                    config.DATA,
                                    "Predictions_VeDBA",#where file-wise predictions are.
                                    dplment,
                                    "*_predictions.csv"
                                )
                            )
        os.makedirs(os.path.join(DEPLOYMENTWISE_INDIVIDUAL_FILES_DEST,
                        dplment), exist_ok=True)

        list_of_inds = list(set(
                        [os.path.basename(x).split("_")[1] for x in all_files]
                        ))
        for ind in list_of_inds:
            list_of_files = [x for x in all_files\
                                if os.path.basename(x).split("_")[1] == ind]
            df_ind = pd.concat((pd.read_csv(x) for x in list_of_files))
            df_ind.to_csv(os.path.join(DEPLOYMENTWISE_INDIVIDUAL_FILES_DEST,
                        dplment, ind + ".csv"), index=False)

if __name__ == "__main__":
    pool_individualwise_predictions()
    pool_deploymentwise_predictions()
