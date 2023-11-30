
# Tags with file corruption

NQ_2021_1/NQ_VNQF020_RRRS_Axy_004_20210811-20210817.csv
corrupted entirely after l.10287211. xxd shows that sensors input only 0s after
this point.

Deleted the last line of this file (l.10287211) with all the 0s in binary,
retained the remaining data.

# Tags that haven't recorded anything

- ZU_2021_2/ZU_VZUM059_LTLS_Axy009_20210718-20210718.csv
- ZU_2021_2/ZU_VZUF052_RRRT_Axy011_20210718-20210718.csv
- ZU_2021_2/ZU_VZUF051_RRTB_Axy022_20210718-20210718.csv

These tags recorded sensor readings of '0' for all time.
Eliminated these files from analyses.
