
# Tags with file corruption

NQ_2021_1/NQ_VNQF020_RRRS_Axy_004_20210811-20210817.csv
corrupted entirely after l.10287211. xxd shows that sensors input only 0s after
this point.

Deleted the last line of this file (l.10287211) with all the 0s in binary,
retained the remaining data.

(2023-12-07) Vlad regenerated this file, so this individual is now included

(2023-12-08) This file isn't in the correct format either, and I will have to
redo the code a lot to accomodate different file structures. I am just skipping
this individual in the interest of time.

# Tags that haven't recorded anything

- ZU_2021_2/ZU_VZUM059_LTLS_Axy009_20210718-20210718.csv
- ZU_2021_2/ZU_VZUF052_RRRT_Axy011_20210718-20210718.csv
- ZU_2021_2/ZU_VZUF051_RRTB_Axy022_20210718-20210718.csv

These tags recorded sensor readings of '0' for all time.
Eliminated these files from analyses.

# VeDBAs are sometimes zero

Some isolated seconds show a VeDBA value of 0. The tag actually doesn't move
around at this time it seems. I am assuming this is a true biological state
where the animal is super-still, because nothing else makes sense to me here.

# After discussion with Vlad

ZU_2021_2
- Eliminating files on 2021-07-18
    - ZU_VZUF054_RRRS_Axy004_20210718-20210718.csv
- Don't consider data from 2021-07-19
- ZU_2021_2 delete all data after 2021-07-25 12:00:00

ZU_2021_1
- deleted ZU_VZUF054_RRRS_Axy003_20210515-20210516.csv because of issue with
  collar and hand
- ZU_VZUF054_RRRS_Axy019_20210517-20210524.csv starts data collection only on
  2021-05-17 around 07:00
- ZU_VZUM056_LTRT_Axy004_20210516-20210518.csv data only after 16 may

RW_2021_1
- start everything 04.06 at 09:00 local
- RW_VJXM126_SHMB_Axy013_20210605-20210606 startd on 05.06.2021 at 09:00local
  time
- RW_VMPF026_RST_Axy019_20210609-20210611.csv start only on 09.06 at 09:00 local
  time

NQ_2021_1
- M019 lost on 13.08
- NQ_VNQM012_SHTB_Axy_009_20210814-20210817.csv should start on 13.08
    BUT (2023-12-08) this file fails totally on the 13th. Is there some
    mislabelling here?
- everything stops after 17.08.2021 stop at 20:00

