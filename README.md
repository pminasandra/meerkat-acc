# meerkat-behaviour-classifier-inator

This repo contains code for predicting meerkat behaviour from accelerometer data.
The raw data used here was obtained as part of the [CCAS](https://movecall.group)
project. This project is described in detail in our
[upcoming pre-print]() and in
our [upcoming paper]().
The members who contributed to the code in this repo are:
- Pranav Minasandra
- Amlan Nayak
- Ariana Strandburg-Peshkin

The folks who worked on this project directly at other parts, including but not limited
to fieldwork, data preprocessing, etc. include:
- Lily Johnson-Ulrich
- Vlad Demartsev
- Marta Manser


# Installation and setup

On Linux and mac, the following command will setup the folder structure
and download and setup code.

```
curl -sSf https://raw.githubusercontent.com/pminasandra/meerkat-acc/master/setup.sh | bash
```

This software was written to analyse meerkat accelerometry data from
collared meerkats. It constructs an elegant machine learning system using
pre-recorded ground truth data, and provides a second-by-second report of 
the behavioural states of the
hyenas. This software, and all libraries used by it, are open source. 

# Details on folder structure

The following folder structure is recommended (and will be setup by the command
above).

```
<PROJECTROOT>/ (usually autonamed meerkat-acc by the command above)
|
|-- classifier/
|-- Data/
|-- Figures/
```

Generally, `PROJECTROOT` can be any folder of your choosing.
In the `classifier` subfolder, you a file named `.cw` that contains _only_ the
filepath for `PROJECTROOT` (also done by the command above).

# Dependencies
The following software components need to be installed.
These will _not_ be installed by the command above, please use the below
instructions.
Commands mentioned work in typical Linux systems running the bash shell (e.g.,
Ubuntu or Pop!\_OS). If you are using Windows or Mac, please install things
using the appropriate way for your system.

## Basic software
Python 3.8+. We have tested on Python 3.10.
To install, use

```
sudo apt install python3
```

## Python libraries
The following python libraries are needed.

- numpy
- scipy
- matplotlib
- pandas
- scikit-learn

To install, you can use

```
python3 -m pip install --user numpy scipy matplotlib pandas scikit-learn
```


# Usage
- Copy the folders `ACC_GPS` and `Audits` (made available [here soon]()) into the
`Data` folder in your `PROJECTROOT`. 
- Run `python3 main.py` to run all analyses in order.

# Contact
If you have any questions or problems with the code, please feel free to contact
me using the methods mentioned on my [website](https://pminasandra.github.io). If your
question is related explicitly to the code, mentioning the make and build of
your OS, and a detailed log of your error, would be very helpful. Have fun with
your analyses!

