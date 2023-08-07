#!/bin/sh

echo "Running action"
export PYTHONPATH="./action"
python -m action $*
echo "Success"
