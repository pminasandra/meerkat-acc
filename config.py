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

ACC_GPS_DIR = os.path.join(DATA, "ACC_GPS")
AUDIT_DIR = os.path.join(DATA, "Audits")
PREDICTIONS_DIR = os.path.join(DATA, "Predictions")

FIGURES = os.path.join(PROJECTROOT, "Figures")

# Deployments
DEPLOYMENTS = ["NQ_2021_1", "RW_2021_1", "ZU_2021_1", "ZU_2021_2"]

# Behavior related config
BEHAVIORS = ["No observation", "Foraging", "Scrabbling", "Standing quadrupedal vigilance",
            "Bipedal vigilance", "Sitting vigilance", "Self groom", "Social",
            "Haunch quadrupedal vigilance", "Walking", "Running", "Processing",
            "Reforage", "Others", "Marking"]

# Other tweaks
formats=['png', 'pdf', 'svg']


# Miscellaneous
SUPPRESS_INFORMATIVE_PRINT = False
