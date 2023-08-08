#!/bin/sh

echo "Activating Python environment"
source activate myenv
# echo out the list files in the current directory
echo "Running action"
ls -la
python -m /path/to/action $*
echo "Success"
