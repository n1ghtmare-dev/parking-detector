#!/bin/bash

export PYTHONPATH="$PWD/src:$PYTHONPATH"
poetry run python3 src/parking_detect/run.py