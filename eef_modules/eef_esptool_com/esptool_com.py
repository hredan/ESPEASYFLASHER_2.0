"""
  esptoo_com.py is a simple python interface to esptool.py (https://github.com/espressif/esptool).
  It is used by ESPEasyFlasher.py to write, read, and erase flash of ESP microcontroller.
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
"""
import os
import esptool


class EsptoolCom:
    """EsptoolCom  ESPEasyFlasher interface to esptool"""
    baud_rate = '460800'
    read_start = '0'
    read_size = '0x400000'
    write_start = '0x00000'
    root_dir = ''

    def esptool_write_eef(self, com_port, write_parameter, content_path):
        """write firmware to flash, with parameter from eef file

            Parameters:
            com_port (str): com port name
            write_parameter (list): esptool parameter
            content_path (str): path of eef and bin files
        """
        command = ['--port', com_port] + write_parameter
        self.run_esptool(command, content_path)

    def esptool_read_flash(self, com_port, filename):
        """read firmware from flash

            Parameters:
            com_port (str): com port name
            filename (str): filename to save read data
        """
        command = ['--port', com_port, '--baud', self.baud_rate,
                   'read_flash', self.read_start, self.read_size, filename]
        self.run_esptool(command)

    def esptool_write_flash(self, com_port, filename):
        """write firmware to flash with config parameter

            Parameters:
            com_port (str): com port name
            filename (str): filename of esp binary
        """
        command = ['--port', com_port, '--baud', self.baud_rate,
                   'write_flash', self.write_start, filename]

        self.run_esptool(command)

    def esptool_erase_flash(self, com_port):
        """erase flash

            Parameters:
            com_port (str): com port name
        """
        command = ['--port', com_port, 'erase_flash']
        self.run_esptool(command)

    def esptool_esp_info(self, com_port, callback):
        """get esp info

            Parameters:
            com_port (str): com port name
            callback (func): callback function to trigger esp selection
        """
        command = ['--port', com_port, 'flash_id']
        self.run_esptool(command)
        callback()

    def run_esptool(self, command, content_path="./ESP_Packages"):
        """run esptool

            Parameters:
            command (list): list of esptool parameter
            content_path (str): path to esp binaries
        """
        print(f'Using command {command}')
        os.chdir(content_path)
        esptool.main(command)
        os.chdir(self.root_dir)
