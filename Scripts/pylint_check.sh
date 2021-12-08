#!/bin/sh
cd ..
pylint espeasyflasher.py
pylint ./eef_modules

read -p "Press enter to continue"
