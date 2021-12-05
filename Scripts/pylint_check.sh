#!/bin/sh
cd ..
pylint espeasyflasher.py

cd eef_modules
pylint `ls -R|grep .py$|xargs`
read -p "Press enter to continue"
