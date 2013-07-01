#!/bin/bash
# sample script with virtualenv
# configure crontab to run this script
cd "$(dirname "$0")"
source $HOME/.virtualenvs/python2.7/bin/activate
python script.py
