#!/bin/sh

echo "Running action"
export PYTHONPATH=$PYTHONPATH:/path/to/module
python -m action $*

echo "Success"
