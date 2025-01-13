# Pranav Minasandra
# Jan 9, 2025
# pminasandra.github.io

# This page exists on a branch of GitHub.
# This runs supplementary code asked by a reviewer for publication,
# and this code is not relevant to the main functioning of this
# classifier. Saved here for rigour and ODS values.

import glob
import os
import os.path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import config

basedir = os.path.join(config.DATA,"Features_VeDBA_2s")
allfiles = glob.glob(os.path.join(basedir, "*/*.csv"))
preddir = os.path.join(config.DATA, "Predictions_VeDBA")

#for file_ in allfiles:
#    print(os.path.basename(file_))
#    df = pd.read_csv(file_)
#    plt.cla()
#    plt.hist(np.log(df["mean_vedba"] + 1e-8), 200)
#    plt.show()

filenames_and_thresholds = {
    "ZU_VZUM056_LTRT_Axy004_20210516-20210518_extracted_features.csv": -2.04,
    "ZU_VZUF051_RRTB_Axy010_20210516-20210524_extracted_features.csv": -1.58,
    "ZU_VZUF054_RRRS_Axy019_20210517-20210524_extracted_features.csv": -2.12,
    "ZU_VZUF052_RRRT_Axy018_20210516-20210524_extracted_features.csv": -1.94,
    "ZU_VZUM057_LTTB_Axy015_20210519-20210524_extracted_features.csv": -1.49,
    "ZU_VZUM057_LTTB_Axy019_20210516-20210516_extracted_features.csv": -1.93,
    "ZU_VZUM053_RRLT_Axy001_20210518-20210524_extracted_features.csv": -2.32,
    "ZU_VZUM059_LTLS_Axy011_20210516-20210523_extracted_features.csv": -1.63,
    "ZU_VZUF052_RRRT_Axy012_20210721-20210725_extracted_features.csv": -1.60,
    "ZU_VZUF052_RRRT_Axy012_20210719-20210720_extracted_features.csv": -1.72,
    "ZU_VZUF051_RRTB_Axy001_20210719-20210725_extracted_features.csv": -1.43,
    "ZU_VZUF054_RRRS_Axy020_20210720-20210722_extracted_features.csv": -1.61,
    "NQ_VNQF014_SHLT_Axy_002_20210811-20210817_extracted_features.csv": -1.63,
    "NQ_VNQM012_SHTB_Axy_009_20210814-20210817_extracted_features.csv": -2.75,#this looks blown
    "NQ_VNQM012_SHTB_Axy_018_20210811-20210813_extracted_features.csv": -1.81,
    "NQ_VNQF013_SHRT_Axy_022_20210811-20210817_extracted_features.csv": -1.65,
    "NQ_VNQM018_RRRT_Axy_020_20210811-20210817_extracted_features.csv": -1.59,
    "RW_VJXM126_SHMB_Axy010_20210604-20210604_extracted_features.csv": -1.71,
    "RW_VJXM122_SHRT_Axy002_20210604-20210611_extracted_features.csv": -2.28,
    "RW_VMPF026_RST_Axy003_20210604-20210608_extracted_features.csv": -1.59,#looks blown
    "RW_VJXM126_SHMB_Axy013_20210605-20210606_extracted_features.csv": -1.56,
    "RW_VMPF029_MBT_Axy004_20210604-20210611_extracted_features.csv": -1.49,
    "RW_VMPF026_RST_Axy019_20210609-20210611_extracted_features.csv": -1.70
    }

for file_ in allfiles:
    print("Classifying", file_)
    bname = os.path.basename(file_)
    tgt = os.path.basename(os.path.dirname(file_))
    tgt = os.path.join(preddir, tgt)
    threshold = filenames_and_thresholds[bname]
    df = pd.read_csv(file_)
    df2 = df.copy()
    df2["state"] = "LOW"
    df2.loc[np.log(df["mean_vedba"] + 1e-8) > threshold, "state"] = "HIGH"
    df2["datetime"] = df2["Timestamp"]
    df2 = df2[["datetime", "state"]]

    bname = bname.replace("extracted_features", "predictions")
    os.makedirs(tgt, exist_ok=True)
    df2.to_csv(os.path.join(tgt, bname), index=False)

