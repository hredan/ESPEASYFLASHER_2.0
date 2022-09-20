#!/bin/bash
git clean -fxd
python3 ./Scripts/build_info.py
python3 -m PyInstaller -F --windowed --add-data "./LogoEasyFlash.png:." --add-data "build_info.txt:." --icon "./resource/macOs/SleepUino.icns" --name ESPEasyFlasher espeasyflasher.py
cp ./ESPEasyFlasherConfig.json ./dist/ESPEasyFlasher.app/Contents/MacOS
cp ./build_info.txt ./dist/ESPEasyFlasher.app/Contents/MacOS
mkdir ./dist/ESPEasyFlasher.app/Contents/MacOS/ESP_Packages
cp ./ESP_Packages/README.md ./dist/ESPEasyFlasher.app/Contents/MacOS/ESP_Packages