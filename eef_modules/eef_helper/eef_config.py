"""
  eef_config contains the class EEFConfig
  It is used by ESPEasyFlasher to read the config from ESPEasyFlasherConfig.json.
  https://github.com/hredan/ESPEASYFLASHER_2.0

  Copyright (C) 2022  André Herrmann (hredan)
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
"""
import os
import sys

import json


class EEFConfig:
    """
    EEFConfig managed the configuration of ESPEasyFlasher
    """
    def __init__(self, config_file, logo_file, str_io, esp) -> None:
        self.__str_io = str_io
        self.__esp = esp
        self.__config_file = config_file
        self.__logo_file = logo_file

        # default config json file
        self.__config_data = {
            "logo": True,
            "devMode": True,
            "serialMonitor": True,
            "espInfo": True
        }

        # more private attributes
        self.__logo_file_path = None
        self.__base_path = None
        self.__is_pyinstaller = self.__check_meipass()
        self.__read_config()

        # check if logo file exists
        if self.with_logo():
            if not self.logo_file_exists():
                self.__config_data["logo"] = False
                self.__logo_file_path = None

    def get_logo_file_path(self):
        """returns logo file path if exists otherwise None"""
        return self.__logo_file_path

    def is_pyinstaller(self):
        """ returns true if executable created by pyinstaller is used"""
        return self.__is_pyinstaller

    def with_developer_mode(self):
        """Config flag to show developer mode control panel in the GUI"""
        return self.__config_data["devMode"]

    def with_logo(self):
        """Config flag to show a logo in the GUI"""
        return self.__config_data["logo"]

    def with_serial_monitor(self):
        """Config flag to show the serial monitor control panel in the GUI"""
        return self.__config_data["serialMonitor"]

    def with_esp_info(self):
        """Config flag to show the esp info button in the GUI"""
        return self.__config_data["espInfo"]

    def get_base_path(self):
        """ returns the root path which contains the eef script or executable"""
        return self.__base_path

    def set_config_data(self, key, data):
        """ copy config data from json data file to member __config_data """
        if key in self.__config_data:
            self.__config_data[key] = data[key]
            self.__str_io.writelines(f"set {key} to\t: {data[key]}\n")
        else:
            raise ValueError("key is not available in config_data")

    def __read_config(self):
        """ read and set the configuration of ESPEasyFlasher from ESPEasyFlasherConfig.json
            ESPEasyFlasherConfig.json has to be in the root directory from espeasyflasher.py.
            If ESPEasyFlasherConfig.json is not available EspEasyFlasher is using some
            default values (not recommended)
        """
        self.__str_io.write("### Read Config ###\n")
        try:
            with open(self.__config_file, encoding="utf-8") as json_file:
                data = json.load(json_file)

                self.set_config_data('logo', data)
                self.set_config_data('devMode', data)
                self.set_config_data('serialMonitor', data)
                self.set_config_data('espInfo', data)

                # set esp config values
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
            # pylint: disable=protected-access
            self.__base_path = sys._MEIPASS
            return_value = True
        except AttributeError:
            self.__base_path = os.path.abspath("..")
            return_value = False

        return return_value

    def logo_file_exists(self):
        """check if logo file exists"""
        return_value = False
        if self.__check_meipass():
            logo_path = os.path.join(self.__base_path, self.__logo_file)
        else:
            logo_path = self.__logo_file

        if os.path.exists(logo_path):
            self.__logo_file_path = logo_path
            return_value = True
        else:
            return_value = False
            self.__str_io.write(
                f"Warning: Could not find '{logo_path}', using layout without logo!\n")

        return return_value
