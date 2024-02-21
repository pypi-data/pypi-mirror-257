#!/bin/sh

flake8 --exclude=.venv
python -m unittest discover -s tests