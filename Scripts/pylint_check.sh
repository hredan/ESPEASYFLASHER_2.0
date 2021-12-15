#!/bin/sh
SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

PYLINT_RC=$BASEDIR/pylint.rc
cd ..
pylint --rcfile=$PYLINT_RC espeasyflasher.py
pylint --rcfile=$PYLINT_RC ./eef_modules

read -p "Press enter to continue"
