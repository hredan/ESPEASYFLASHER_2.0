#!/bin/sh
cd ..
pylint ./eef_modules
pylint espeasyflasher.py
read -p "Press enter to continue"
