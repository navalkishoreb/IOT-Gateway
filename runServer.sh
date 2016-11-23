#!/bin/bash
source ./venv/bin/activate
clear
python dashboard.py runserver -h 0.0.0.0 -p 80 --debug --reload
