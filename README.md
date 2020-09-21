# Duwo Laundry Stats

This project gathers data from duwo.multiposs.nl and analyses the machine
availability.

# How to use

The project has 2 parts:

 - The scraper bot (`scraper.py`)
 - The analysis script (`main.py`)

## The scraper bot

The `scraper.py` script will log on to the site and log the availability into a
file. It should run periodically (like every 5 minutes) on a server (i use a
raspberry pi)

### Install

Copy the script to a server:

`scp scraper.py [server]:~/scraper.py`

Make it run every 5 minutes:

 - run `crontab -e`
 - add: `*/5 * * * * ~/scraper.py`

That's it, now the `~/laundry_stats` file will slowly accumulate the
laundry availability data.

## The analysis script

Running the analysis and generating the scripts has been made as simple as
possible. If you want to understand the project better and improve it, look into
the Makefile.

### Requirements

 - python
 - pipenv (or pandas, numpy and matplotlib) this tutorial assumes pipenv
 - the data from the scraper

### Running the analysis

Copy the data to the root of the project (call it `data`):

`scp [server]:~/laundry_stats ./data`

Install the python environment and dependencies:

`pipenv install`

Run the analysis:

`make`

or seperately:

```
mkdir plots

pipenv run python main.py

cp data plots/data.txt
zip -r laundry_plots.zip plots
```


# Contributing and extra info

If you want to understand the project better or help improve it, look into the
Makefile.

I use:
 - Jupyter Notebook for development
    - this gets compiled to main.py using `make build`
 - Pipenv for dependencies
 - A raspberry pi to run the scraper

If you have questions you can DM me.
