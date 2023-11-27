# Pranav Minasandra
# pminasandra.github.io
# Nov 27, 2023

"""
Due to inconsistencies in Amlan's implementation of the code and due to errors
in file handling, naming, and storage, this code is necessary to fix these
issues. This is one-time-use code, and must NOT be run again. This is committed
on GitHub for diagnostic reasons.
"""

import glob
import os.path

import pandas as pd

import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

def alert_and_prompt():
    print("this code needs to be run only once, to fix potential issues with files.")
    print("if file issues are already fixed, running this code is unnecessary and may harm your files.")
    input("press enter to continue, or Ctrl+C to exit.")


def exterminate_extraneous_column():
    """
    The label files stored by Amlan contain an extra column without a label.
    This code deletes this extra column
    """
    alert_and_prompt()

    for dplment in config.DEPLOYMENTS:
        tgtpath = os.path.join(config.AUDIT_DIR, dplment)
        for csvfilepath in glob.glob(os.path.join(tgtpath, "*.csv")):
            csvfile = pd.read_csv(csvfilepath, index_col=[0])
            csvfile.to_csv(csvfilepath, index=False)

if __name__ == "__main__":
#    exterminate_extraneous_column() # already done, don't re-do
