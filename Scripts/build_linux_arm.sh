#!/bin/bash
cat > /etc/pip.conf << EOF
[global]
extra-index-url=https://www.piwheels.org/simple
EOF

python3 -m venv /home/venv
source /home/venv/bin/activate

pip install -r requirements.txt
python ./Scripts/build_info.py -s $GIT_HASH -r $GIT_URL -n $GIT_NAME
python -m PyInstaller -F --collect-data esptool --add-data "./LogoEasyFlash.png:." --add-data "build_info.txt:." --name ESPEasyFlasher espeasyflasher.py
cp ./ESPEasyFlasherConfig.json ./dist
cp ./build_info.txt ./dist
mkdir ./dist/ESP_Packages
cp ./ESP_Packages/README.md ./dist/ESP_Packages