# Pranav Minasandra
# pminasandra.github.io
# November 27, 2023

"""
Configuration for rest of code.
"""

import os
import os.path

# Directories
with open(".cw", "r") as fd:
    PROJECTROOT = fd.read().rstrip()
DATA = os.path.join(PROJECTROOT, "Data")

ACC_GPS_DIR = "/home/pranav/ExtraneousData/Meerkats/ACCGPS"
AUDIT_DIR = os.path.join(DATA, "Audits")
PREDICTIONS_DIR = os.path.join(DATA, "Predictions")

FIGURES = os.path.join(PROJECTROOT, "Figures")

# Deployments
#DEPLOYMENTS = ["NQ_2021_1", "RW_2021_1", "ZU_2021_1", "ZU_2021_2"]

DEPLOYMENTS = ["NQ_2021_1",
"NQ_2022_1",
"RW_2021_1",
"RW_2022_1",
"SI_2022_1",
"ZU_2021_1",
"ZU_2021_2",
"L_2024_2"]

# Loading names of all individuals
INDIVIDUALS = {}
for dplment in DEPLOYMENTS:
    dirname = os.path.join(ACC_GPS_DIR, dplment)
    if dplment not in INDIVIDUALS:
        INDIVIDUALS[dplment] = []

    for filename in os.listdir(dirname):
        INDIVIDUALS[dplment].append(filename.split('_')[1])

for dplment in INDIVIDUALS:
    INDIVIDUALS[dplment] = list(set(INDIVIDUALS[dplment]))

# Behavior related config
BEHAVIORS = ["No observation", "Foraging", "Scrabbling", "Standing quadrupedal vigilance",
            "Bipedal vigilance", "Sitting vigilance", "Self groom", "Social",
            "Haunch quadrupedal vigilance", "Walking", "Running", "Processing",
            "Reforage", "Others", "Marking"]

DROP_MISSING = True
COMBINE_BEHAVIORS = True
DROP_OTHERS = True

BEHAVIOR_SIMPLIFIER = {
    'Vigilance': 'Vigilance',
    'Sitting vigilance': 'Vigilance',
    'Bipedal vigilance': 'Vigilance',
    'Haunch quadrupedal vigilance': 'Vigilance',
    'Standing quadrupedal vigilance': 'Vigilance',
    'Foraging': 'Foraging',
    'Scrabbling': 'Foraging',
    'Walking': 'Foraging',
    'Reforage': 'Foraging',
    'Others': 'Others',
    'Social': 'Others',
    'Processing': 'Others',
    'Self groom': 'Others',
    'Marking': 'Others',
    'Running': 'Running'
} # comes from repeated tweaking during Amlan's project

# Other tweaks
formats=['png', 'pdf', 'svg']


# Miscellaneous
SUPPRESS_INFORMATIVE_PRINT = False
AMLAN_OFFSET = -4 # There is a strange inexplicable offset between the ACC and
                  # the official labels
LOG_TRANSFORM_VEDBA = True
SCALE_DATA = False # turned out to be a bad idea
