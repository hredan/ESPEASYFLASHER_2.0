"""
  esp_func_calls.py is used by ESPEasyFlasher.py to support esptool functionality.
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
import json
import shutil
import zipfile
import threading
import re


# pylint: disable=too-few-public-methods
class EspFuncCalls:
    """
    EspFuncCalls contains functions to run esptool actions in a separate thread
    """

    def __init__(self, public_gui_elements, esp_com, label_frames) -> None:
        self.__public_gui_elements = public_gui_elements
        self.label_frames = label_frames
        self.__esp_com = esp_com

    # R0913: Too many arguments (6/5) (too-many-arguments)
    # in this case allow more than 5 arguments, it is needed here
    # pylint: disable=R0913
    def __base_thread(self, target_method, info_text, set_progressbar=False,
                      second_arg=None, third_arg=None):
        """base thread"""
        os.chdir(self.__esp_com.root_dir)
        print(f"Info: CWD {os.getcwd()}")
        if set_progressbar:
            progress_bar = self.__public_gui_elements.get_progress_bar()
            progress_bar["value"] = 0
            progress_bar["maximum"] = 100

        # Disable Serial Monitor if enabled
        self.__public_gui_elements.get_frame_serial_monitor().disable_serial_monitor()

        print(info_text)
        com_port = self.label_frames.get_com_port()
        if com_port == "":
            print("Error: select a Serial Com Port before you can start read flash!")
        else:
            if third_arg:
                thread = threading.Thread(target=target_method, args=(
                    com_port, second_arg, third_arg,))
            elif second_arg:
                thread = threading.Thread(target=target_method,
                                          args=(com_port, second_arg,))
            else:
                thread = threading.Thread(
                    target=target_method, args=(com_port,))
            thread.start()

    def esp_info_callback(self):
        """ Callback function for esp threads"""
        stdout_redirection = self.__public_gui_elements.get_stdout_redirection()
        print(f"Detected ESP of type: {stdout_redirection.esp_type}, " +
              f"with Flash Size of: {stdout_redirection.esp_flash_size}")
        file_list = []
        if stdout_redirection.esp_type:

            for entry in self.label_frames.get_file_list_combo_write():
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
        stdout_redirection = self.__public_gui_elements.get_stdout_redirection()
        stdout_redirection.esp_type = None
        stdout_redirection.esp_flash_size = None
        self.__base_thread(self.__esp_com.esptool_esp_info,
                           "### ESP INFO ###", False, self.esp_info_callback)

    def erase_flash(self):
        """erase ESP flash"""
        self.__base_thread(self.__esp_com.esptool_erase_flash, "### Erase Flash ###")

    def write_flash(self):
        """ write data to ESP flash"""
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
                                   "### Write Flash ###", True, command, content_path)
            elif file_extension == ".zip":
                extract_path = f"{root_dir}/ESP_Packages/Extracted"
                zip_path = f"{root_dir}/ESP_Packages/{filename}"
                eef_path = f"{root_dir}/ESP_Packages/Extracted/{file_name}.eef"
                # make dir, if exist clear content of dir
                if os.path.exists(extract_path):
                    shutil.rmtree(extract_path)
                else:
                    os.mkdir(extract_path)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                if os.path.exists(eef_path):
                    print(f"Info: eef file path: {eef_path}")
                    command = EspFuncCalls.__read_eef_file(eef_path)
                    self.__base_thread(
                        self.__esp_com.esptool_write_eef, "### Write Flash ###",
                        True, command, extract_path)
                else:
                    print(
                        f"Error: WriteFlash->could not find eef file, expected {eef_path}")

            else:
                self.__base_thread(self.__esp_com.esptool_write_flash,
                                   "### Write Flash ###", True, filename)

    def read_flash(self):
        """ read ESP flash"""
        filename = self.label_frames.get_read_file_name()
        if filename == "":
            print("Error: before you can read flash, define a filename")
        else:
            filename = filename + ".bin"
            self.__base_thread(self.__esp_com.esptool_read_flash,
                               "### Read Flash ###", True, filename)

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
