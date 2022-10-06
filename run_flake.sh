#!/bin/sh
# Exits zero if there is passed argument to the script
EXITS_ZERO="--exit-zero"
MAX_LINE="127"
if [ -z "$1" ]
  then
    echo "Run  argument is null"
    EXITS_ZERO=""
fi
flake8 . --exclude .git,.venv,*migrations* --count --show-source --statistics --max-line-length=$MAX_LINE $EXITS_ZERO
