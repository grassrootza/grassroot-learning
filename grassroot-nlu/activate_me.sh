#!/bin/sh

export FLASK_APP=start_application.py
flask run > output.txt 2>&1 &
