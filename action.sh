#!/bin/sh

echo "Running action"
ls
python action/__main__.py $*
echo "Success"
