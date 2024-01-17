#!/bin/bash
#
# Pranav Minasandra
# pminasandra.github.io
# July 26, 2023
#
# Usage:
# curl -sSf https://raw.githubusercontent.com/pminasandra/bout-duration-distributions/master/setup.sh | bash

mkdir meerkat-acc
cd meerkat-acc

git clone https://github.com/pminasandra/meerkat-acc classifier

mkdir Data
mkdir Data/ClassifierRelated
mkdir Data/Features
mkdir Data/Predictions
mkdir Data/PredictionsByIndividual
mkdir Data/PredictionsByIndividualDeploymentwise

mkdir Figures

echo $PWD > classifier/.cw
