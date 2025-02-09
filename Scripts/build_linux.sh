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

if [ -n "$GITHUB_REF_NAME" ]
then
    GIT_NAME=$GITHUB_REF_NAME
else
    GIT_NAME=$(git rev-parse --abbrev-ref HEAD)
fi

pip install -r requirements.txt
python ./Scripts/build_info.py -s $GIT_HASH -r $GIT_URL -n $GIT_NAME
python -m PyInstaller -F --collect-data esptool --add-data "./LogoEasyFlash.png:." --add-data "build_info.txt:." --name ESPEasyFlasher espeasyflasher.py
cp ./ESPEasyFlasherConfig.json ./dist
cp ./build_info.txt ./dist
mkdir ./dist/ESP_Packages
cp ./ESP_Packages/README.md ./dist/ESP_Packages