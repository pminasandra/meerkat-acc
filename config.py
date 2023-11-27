
# Pranav Minasandra
# pminasandra.github.io
# November 27, 2023

import os
import os.path


# Directories
PROJECTROOT = open(".cw", "r").read().rstrip()
DATA = os.path.join(PROJECTROOT, "Data")

ACC_GPS_DIR = os.path.join(DATA, "ACC_GPS")
AUDIT_DIR = os.path.join(DATA, "Audits")
PREDICTIONS_DIR = os.path.join(DATA, "Predictions")

FIGURES = os.path.join(PROJECTROOT, "Figures")

# Deployments
DEPLOYMENTS = ["NQ_2021_1", "RW_2021_1", "ZU_2021_1", "ZU_2021_2"]

# Other tweaks
formats=['png', 'pdf', 'svg']


# Miscellaneous
SUPPRESS_INFORMATIVE_PRINT = False
