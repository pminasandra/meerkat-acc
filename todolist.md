# To do

- [x] preprocessing.py fix inconsistencies in file scheme
- [x] auditreading.py read labels
- [x] accreading.py read ACC data
    - [x] accreading.py trim 0s, convert to NaNs
    - [x] accreading.py implement generator
- [x] extractor.py feature extraction functions
- [x] classifier.py file naming bug resolution
- [x] classifier.py put all the data together
- [x] classifier.py full classification using RF
- [x] analyses.py generate confusion matrices, precision-recall tables


# Decided were probably irrelevant

- [ ] accreading.py recast to 3D arrays.
    No need, feature extraction works superfast anyway
- [ ] gps_speeds.py extract GPS running states.
    We will replace this with a bunch more running labels from the 2022 dataset.
