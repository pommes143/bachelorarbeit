#!/bin/sh
virtualenv --python python3 .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip list

chmod a+x execute_text.sh
chmod a+x start.sh