#!/bin/sh
# Bez argumentow albo z True ma zwrocic kod
# w innym przypadku exit zero

EXITS_ZERO="--exit-zero"

MAX_LINE="127"
if [ -z "$1" ] || [ $1 = "true" ]  || [ $1 = "True" ]
  then
  EXITS_ZERO=""
else
  
  EXITS_ZERO="--exit-zero"
fi
test -z $EXITS_ZERO && echo "Ill break on lining" || echo "I am not breaking on lining"
flake8 . --exclude .git,.venv,*migrations* --count --show-source --statistics --max-line-length=$MAX_LINE $EXITS_ZERO

exit $?