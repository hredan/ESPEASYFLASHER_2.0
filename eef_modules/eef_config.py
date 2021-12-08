'''
  eef_config contains the class EEFConfig
  It is used by ESPEasyFlasher to read the config from ESPEasyFlasherConfig.json.
  https://github.com/hredan/ESPEASYFLASHER_2.0

  Copyright (C) 2021  André Herrmann (hredan)
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import sys

import json

class EEFConfig:
    """
    EEFConfig managed the configuration of ESPEasyFlasher
    """
    def __init__(self, str_io, esp) -> None:
        self.__str_io = str_io
        self.__esp = esp
        # default config
        self.__developer_mode = True
        self.__with_logo = True
        self.__with_serial_monitor = True
        self.__with_esp_info = True
        self.__logo_file_path = None

        self.__is_pyinstaller = self.__check_meipass()
        self.__read_config()

        # check if logo file exists
        if self.__with_logo:
            if not self.logo_file_exists():
                self.__with_logo = False
                self.__logo_file_path = None

    def get_logo_file_path(self):
        """returns logo file path if exists otherwise None"""
        return self.__logo_file_path

    def is_pyinstaller(self):
        """ returns true if executable created by pyinstaller is used"""
        return self.__is_pyinstaller

    def with_developer_mode(self):
        """Config flag to show developer mode control panel in the GUI"""
        return self.__developer_mode

    def with_logo(self):
        """Config flag to show a logo in the GUI"""
        return self.__with_logo

    def with_serial_monitor(self):
        """Config flag to show the serial monitor control panel in the GUI"""
        return self.__with_serial_monitor

    def with_esp_info(self):
        """Config flag to show the esp info button in the GUI"""
        return self.__with_esp_info

    def get_base_path(self):
        """ returns the root path which contains the eef script or executable"""
        return self.__base_path

    def __read_config(self):
        """ read and set the configuration of ESPEasyFlasher from ESPEasyFlasherConfig.json
            ESPEasyFlasherConfig.json has to be in the root directory from espeasyflasher.py.
            If ESPEasyFlasherConfig.json is not available EspEasyFlasher is using some
            default values (not recommended)
        """
        self.__str_io.write("### Read Config ###\n")
        try:
            with open('ESPEasyFlasherConfig.json', encoding="utf-8") as json_file:
                data = json.load(json_file)

                self.__with_logo = data['logo']
                self.__str_io.writelines(f"enable logo: {data['logo']}\n")

                self.__developer_mode = data['devMode']
                self.__str_io.writelines(f"dev mode is: {data['devMode']}\n")

                self.__with_serial_monitor = data['serialMonitor']
                self.__str_io.writelines(
                    f"serial monitor: {data['serialMonitor']}\n")

                self.__with_esp_info = data['espInfo']
                self.__str_io.writelines(f"esp info: {data['espInfo']}\n")

                self.__esp.baud_rate = data['baudRate']
                self.__str_io.write(f"set baud rate to: {data['baudRate']}\n")

                self.__esp.read_start = data['readStart']
                self.__str_io.write(f"set read start to: {data['readStart']}\n")

                self.__esp.read_size = data['readSize']
                self.__str_io.write(f"set read size to: {data['readSize']}\n")

                self.__esp.write_start = data['writeStart']
                self.__str_io.write(f"set write start to: {data['writeStart']}\n")

        except EnvironmentError as err:
            self.__str_io.writelines(
                f"Error could not read config, default values will be used: {err}\n")


    def __check_meipass(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        return_value = False
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            # pylint: disable=E1101
            # pylint: disable=W0212
            self.__base_path = sys._MEIPASS
            return_value = True
        except AttributeError:
            self.__base_path = os.path.abspath(".")
            return_value = False

        return return_value

    def logo_file_exists(self):
        """check if logo file exists"""
        return_value = False
        filename = "./LogoEasyFlash.png"
        if os.path.exists(filename):
            self.__logo_file_path = filename
            return_value = True
        elif self.__check_meipass():
            self.__logo_file_path = os.path.join(self.__base_path, filename)
            return_value = True
        else:
            return_value = False
            self.__str_io.write(
                f"Warning: Could not find '{filename}', using layout without logo!\n")

        return return_value
