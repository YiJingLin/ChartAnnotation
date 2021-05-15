#!/bin/bash

if [ -d ".venv" ]
then
    . .venv/bin/activate
    pip3 install -r requirements.txt
    python3 wsgi.py
else
    python3 -m venv .venv
    . .venv/bin/activate
    python3 -m pip install --upgrade pip
    pip3 install -r requirements.txt
    python3 wsgi.py
fi
