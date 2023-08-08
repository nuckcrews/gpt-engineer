#!/bin/sh

echo "Activating Python environment"
source activate myenv

echo "Running action"
python -m /path/to/action $*

echo "Success"
