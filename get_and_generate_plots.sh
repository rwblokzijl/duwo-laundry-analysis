#!/bin/bash

# Clear old outputs and data, so we error properly when stale
rm data
rm plots/*
rm laundry_plots.zip

# Prepare data, script and environment
scp git.blokzijl.family:both ./data
jupyter nbconvert --to script main.ipynb
pipenv install

# Generate output
pipenv run python main.py

# Bundle output
cp data plots/data.txt
zip -r laundry_plots.zip plots
