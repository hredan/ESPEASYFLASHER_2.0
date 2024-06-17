"""
  write_flash.py is used by ESPEasyFlasher.py to create and handle Write Label Frame.
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
import glob
import tkinter as tk
from tkinter import ttk

from eef_modules.eef_esptool_com.esp_func_calls import EspFuncCalls

ESP_PACKAGES = "./ESP_Packages"
class WriteLabelFrame(tk.LabelFrame):
    """
    Class to create and handle the Write Label Frame
    """

    def __init__(self, frame):
        super().__init__(frame, text='WriteFlash')
        self.__combo_write_flash = ttk.Combobox(self)
        self.file_list = []

    def set_positioning(self, row_pos_frame, esp_func_calls:EspFuncCalls) -> None:
        """ define and initialize elements of Write Label Frame """
        self.grid(column=0, row=row_pos_frame, columnspan=3, sticky="EW", padx=5, pady=5)

        row_pos_write = 0
        label_write_flash = tk.Label(self, text="binary file/package: ")
        label_write_flash.grid(column=0, row=row_pos_write, sticky="W")

        self.get_file_list()
        self.set_file_list_combo_write(self.file_list)
        self.__combo_write_flash.grid(column=1, row=row_pos_write,
                                      sticky="EW", padx=3, pady=3)

        row_pos_write += 1
        button = tk.Button(self, text="WriteFlash", command=esp_func_calls.write_flash)
        button.grid(column=0, row=row_pos_write, columnspan=2, sticky="EW", padx=3, pady=3)

        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=2)

    def set_file_list_combo_write(self, file_list):
        """set file list for combobox write flash"""
        self.__combo_write_flash["values"] = file_list
        if len(file_list) > 0:
            self.__combo_write_flash.current(0)

    def get_file_list_combo_write(self):
        """get the file list of the combobox"""
        return self.__combo_write_flash["values"]

    def get_file_name(self):
        """get the selected file name in the combobox"""
        return self.__combo_write_flash.get()

    def get_file_list(self):
        """get file list for write combobox, depends on file extension,
        can be zip (ESPEasyFlasher Package)
        eef files with required bin files
        or only a bin for a ESP8266"""
        file_list = glob.glob("*.zip", root_dir=ESP_PACKAGES)
        file_list.extend(glob.glob("*.eep", root_dir=ESP_PACKAGES))
        if len(file_list) == 0:
            file_list = glob.glob("*.eef", root_dir=ESP_PACKAGES)
            if len(file_list) == 0:
                file_list = glob.glob("*.bin", root_dir=ESP_PACKAGES)
        self.file_list = file_list
        return file_list
