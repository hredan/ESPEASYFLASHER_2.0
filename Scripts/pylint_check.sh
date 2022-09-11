#!/bin/sh
SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

PYLINT_RC=$BASEDIR/pylint.rc
cd ..
pylint --rcfile=$PYLINT_RC espeasyflasher.py
pylint --rcfile=$PYLINT_RC ./eef_modules
pylint --rcfile=$PYLINT_RC ./tests
pylint --rcfile=$PYLINT_RC ./Scripts/build_info.py

read -p "Press enter to continue"
