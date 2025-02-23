"""
  esp_func_calls.py is used by ESPEasyFlasher.py to support esptool functionality.
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
import json
import zipfile
import threading
import re
import tempfile

from eef_modules.eef_esptool_com.esptool_com import EsptoolCom
class EspFuncCalls:
    """
    EspFuncCalls contains functions to run esptool actions in a separate thread
    """

    def __init__(self, bottom_gui_elements, esp_com:EsptoolCom, label_frames) -> None:
        self.__bottom_gui_elements = bottom_gui_elements
        self.label_frames = label_frames
        self.__esp_com = esp_com
        self.thread = None

    # R0913: Too many arguments (6/5) (too-many-arguments)
    # in this case allow more than 5 arguments, it is needed here
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-arguments
    def __base_thread(self, target_method, info_text,
                      second_arg=None, third_arg=None, fourth_arg=None):
        """base thread"""
        os.chdir(self.__esp_com.root_dir)
        print(f"Info: CWD {os.getcwd()}")

        # Disable Serial Monitor if enabled
        self.__bottom_gui_elements.disable_serial_monitor()

        print(info_text)
        com_port = self.label_frames.get_com_port()
        if com_port == "":
            print("Error: select a Serial Com Port before you can start read flash!")
        elif self.thread and self.thread.is_alive():
            # do not start a new thread if a thread is already running
            return
        else:
            if third_arg:
                self.thread = threading.Thread(target=target_method, args=(
                    com_port, second_arg, third_arg,))
            elif second_arg:
                self.thread = threading.Thread(target=target_method,
                                          args=(com_port, second_arg,))
            elif fourth_arg:
                self.thread = threading.Thread(target=target_method,
                                          args=(com_port, second_arg, third_arg, fourth_arg,))
            else:
                self.thread = threading.Thread(
                    target=target_method, args=(com_port,))
            self.thread.start()

    def get_eef_path(self, extract_path):
        """get eef file path from extract path"""
        eef_files = []
        for file in os.listdir(extract_path):
            if file.endswith(".eef"):
                eef_files.append(file)
        if len(eef_files) > 1:
            print("warning: Multiple eef files found in zip/eep file")
        elif len(eef_files) == 0:
            print("Error: No eef file found in zip/eep file")
            return None
        return os.path.join(extract_path, eef_files[0])

    def esp_info_callback(self):
        """ Callback function for esp threads"""
        stdout_redirection = self.__bottom_gui_elements.stdout_redirection
        print(f"Detected ESP of type: {stdout_redirection.esp_type}, " +
              f"with Flash Size of: {stdout_redirection.esp_flash_size}")
        file_list = []
        if stdout_redirection.esp_type:

            for entry in self.label_frames.get_file_list():
                if re.match(f"^{stdout_redirection.esp_type}", entry, re.IGNORECASE):
                    file_list.append(entry)

            if len(file_list) > 0:
                self.label_frames.set_file_list_combo_write(file_list)
                print(f"Filter {stdout_redirection.esp_type} files")
            else:
                print(
                    f"[War] Could not find entries for {stdout_redirection.esp_type}")

    def get_esp_info(self):
        """ESP Info request"""
        stdout_redirection = self.__bottom_gui_elements.stdout_redirection
        stdout_redirection.esp_type = None
        stdout_redirection.esp_flash_size = None
        self.__base_thread(self.__esp_com.esptool_esp_info,
                           "### ESP INFO ###", self.esp_info_callback)

    def erase_flash(self):
        """erase ESP flash"""
        self.__base_thread(self.__esp_com.esptool_erase_flash, "### Erase Flash ###")

    def write_flash(self):
        """ write data to ESP flash"""
        extract_path=None
        filename = self.label_frames.get_filename_write()
        if filename == "":
            print("Error: before you can write to flash, select a firmware.bin file")
        else:
            file_name, file_extension = os.path.splitext(filename)
            root_dir = self.__esp_com.root_dir
            if file_extension == ".eef":
                content_path = f"{root_dir}/ESP_Packages"
                eef_path = f"{content_path}/{filename}"
                print(f"Info: eef file path: {eef_path}")
                command = self.__read_eef_file(eef_path)
                self.__base_thread(self.__esp_com.esptool_write_eef,
                                   "### Write Flash ###", command, content_path)
            elif file_extension in ('.zip', '.eep'):
                extract_path = tempfile.mkdtemp()
                zip_path = f"{root_dir}/ESP_Packages/{filename}"

                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                eef_path = self.get_eef_path(extract_path)
                if os.path.exists(eef_path):
                    print(f"Info: eef file path: {eef_path}")
                    command = EspFuncCalls.__read_eef_file(eef_path)
                    self.__base_thread(
                        self.__esp_com.esptool_write_eef, "### Write Flash ###", command, extract_path)
                else:
                    print(
                        f"Error: WriteFlash->could not find eef file, expected {eef_path}")
            else:
                self.__base_thread(self.__esp_com.esptool_write_flash,
                                   "### Write Flash ###", filename)

    def read_flash(self):
        """ read ESP flash"""
        filename = self.label_frames.get_read_file_name()
        if filename == "":
            print("Error: before you can read flash, define a filename")
        else:
            filename = filename + ".bin"
            self.__base_thread(self.__esp_com.esptool_read_flash,
                               "### Read Flash ###", filename)

    @staticmethod
    def __read_eef_file(filename):
        """read esptool parameter settings from eef file"""
        print("### read eef file ###")
        return_value = ""
        try:
            with open(filename, encoding="utf-8") as json_file:
                data = json.load(json_file)
                return_value = data['command']

        except EnvironmentError as err:
            print(f"Error could not read eef file {filename}: {err}")
        return return_value
