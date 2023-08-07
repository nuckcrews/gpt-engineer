#!/bin/sh

echo "Running action"
# echo out the list files in the current directory
ls -la
ls -l
python -m action $*
echo "Success"
