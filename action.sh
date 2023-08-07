#!/bin/sh

echo "Running action"
sh pip list
exec python -m action $*
echo "Success"
