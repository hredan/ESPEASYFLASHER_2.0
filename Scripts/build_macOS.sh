#!/bin/bash
# if $GITHUB_REPOSITORY is available, then script is running in GitHub Actions on GitHub Runner
if [ -n "$GITHUB_REPOSITORY" ]
then
    GIT_URL="www.github.com/${GITHUB_REPOSITORY}"
else
    GIT_URL=$(git config --get remote.origin.url)
fi

if [ -n "$GITHUB_SHA" ]
then
    GIT_HASH=$GITHUB_SHA
else
    GIT_HASH=$(git rev-parse HEAD)
fi

python3 ./Scripts/build_info.py -s $GIT_HASH -r $GIT_URL
python3 -m PyInstaller -F --windowed --collect-data esptool --add-data "./LogoEasyFlash.png:." --add-data "build_info.txt:." --icon "./resource/macOs/SleepUino.icns" --name ESPEasyFlasher espeasyflasher.py
cp ./ESPEasyFlasherConfig.json ./dist/ESPEasyFlasher.app/Contents/MacOS
cp ./build_info.txt ./dist/ESPEasyFlasher.app/Contents/MacOS
mkdir ./dist/ESPEasyFlasher.app/Contents/MacOS/ESP_Packages
cp ./ESP_Packages/README.md ./dist/ESPEasyFlasher.app/Contents/MacOS/ESP_Packages
rm ./dist/ESPEasyFlasher
chmod +x ./dist/ESPEasyFlasher.app/Contents/MacOS/ESPEasyFlasher
