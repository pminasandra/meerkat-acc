# Pranav Minasandra
# pminasandra.github.io
# Nov 27, 2023

"""
Due to inconsistencies in Amlan's implementation of the code and due to errors
in file handling, naming, and storage, this code is necessary to fix these
issues. This is one-time-use code, and must NOT be run again. This is committed
on GitHub for diagnostic reasons.
"""

import datetime as dt
import glob
import os.path

import pandas as pd

import accreading
import config
import utilities

if not config.SUPPRESS_INFORMATIVE_PRINT:
    old_print = print
    print = utilities.sprint

def _alert_and_prompt():
    print("this code needs to be run only once, to fix potential issues with files.")
    print("if file issues are already fixed, running this code is unnecessary\
         and may harm your files.")
    input("press enter to continue, or Ctrl+C to exit.")


def exterminate_extraneous_column():
    """
    The label files stored by Amlan contain an extra column without a label.
    This code deletes this extra column.
    """
    _alert_and_prompt()

    for dplment in config.DEPLOYMENTS:
        tgtpath = os.path.join(config.AUDIT_DIR, dplment)
        for csvfilepath in glob.glob(os.path.join(tgtpath, "*.csv")):
            csvfile = pd.read_csv(csvfilepath, index_col=[0])
            csvfile.to_csv(csvfilepath, index=False)


def delete_useless_data():
    """
    A lot of the data come from collars before or after they were deployed.
    Speaking to Vlad, I have arrived at which data need to be exterminated.
    Refer project-notes.md
    """
    # this function is just a big hack
    # rewrite it every single time new data is added

    accgen = accreading.load_acc_files(subset_cols=False)
    for dplment, filename, df in accgen:
        print(f"processing {filename}")
        if dplment == 'NQ_2021_1':
            df = df[df['Timestamp'] < dt.datetime(2021, 8, 17, 20, 0, 0)]
            df = df[df['Timestamp'] > dt.datetime(2021, 8, 11, 7, 0, 0)]
            print("general data trimming")

            if 'M019' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] < dt.datetime(2021, 8, 13,
                                                        0, 0, 0)]
            if 'VNQM012_SHTB_Axy_009' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] > dt.datetime(2021, 8, 13,
                                                        7, 0, 0)]
            if 'VNQM012_SHTB_Axy_013' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] < dt.datetime(2021, 8, 13,
                                                        7, 0, 0)]

        elif dplment == "RW_2021_1":
            print("general data trimming")
            df = df[df['Timestamp'] > dt.datetime(2021, 6, 4, 7, 0, 0)]
            df = df[df['Timestamp'] < dt.datetime(2021, 6, 11, 7, 0, 0)]

            if 'VJXM126_SHMB_Axy013' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] > dt.datetime(2021, 6, 5,
                                                        7, 0, 0)]
            if 'VJXM126_SHMB_Axy010' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] < dt.datetime(2021, 6, 5,
                                                        6, 50, 0)]
            if 'VMPF026_RST_Axy019' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] > dt.datetime(2021, 6, 9,
                                                        7, 0, 0)]
            if 'VMPF026_RST_Axy003' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] < dt.datetime(2021, 6, 9,
                                                        7, 0, 0)]

        elif dplment == "ZU_2021_1":
            df = df[df['Timestamp'] > dt.datetime(2021, 5, 16, 7, 0, 0)]
            df = df[df['Timestamp'] < dt.datetime(2021, 5, 24, 7, 0, 0)]
            print("general data trimming")
            if 'VZUF054_RRRS_Axy019' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] > dt.datetime(2021, 5, 17,
                                                        7, 0, 0)]
            if 'VZUM056_LTRT_Axy004' in filename:
                print("ind-specific data dropping")
                df = df[df['Timestamp'] > dt.datetime(2021, 5, 16,
                                                        7, 0, 0)]

        elif dplment == "ZU_2021_2":
            df = df[df['Timestamp'] > dt.datetime(2021, 7, 18, 7, 0, 0)]
            df = df[df['Timestamp'] < dt.datetime(2021, 7, 25, 7, 0, 0)]
            print("general data trimming")
            df = df[df['Timestamp'] < dt.datetime(2021, 7, 25, 10, 0, 0)]
            df = df[df['Timestamp'].dt.date != dt.date(2021, 7, 19)]

        df['Timestamp'] = df['Timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S.%f')
        tgtfilename = os.path.join(config.ACC_GPS_DIR, dplment, filename)
        df.to_csv(tgtfilename + ".csv", index=False)

if __name__ == "__main__":
    delete_useless_data()
    pass
#    exterminate_extraneous_column() # already done, don't re-do
