#!/bin/sh -l

echo "Running action"
sh -c "python -m action $*"
echo "Success"
