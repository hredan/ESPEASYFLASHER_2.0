'''
  label_frame_write_flash.py is used by ESPEasyFlasher.py to create and handle Write Label Frame.
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
import tkinter as tk
from tkinter import ttk


class WriteLabelFrame:
    """
    Class to create and handle the Write Label Frame
    """

    def __init__(self, frame, row_pos_frame, file_list, esp_func_calls) -> None:
        write_group = tk.LabelFrame(frame, text='WriteFlash')
        write_group.grid(column=0, row=row_pos_frame,
                         columnspan=3, sticky="EW", padx=5, pady=5)

        row_pos_write = 0
        label_write_flash = tk.Label(write_group, text="bin file: ")
        label_write_flash.grid(column=0, row=row_pos_write, sticky="W")

        self.__combo_write_flash = ttk.Combobox(write_group)

        self.set_file_list_combo_write(file_list)
        self.__combo_write_flash.grid(column=1, row=row_pos_write,
                                      sticky="EW", padx=3, pady=3)

        row_pos_write += 1
        button = tk.Button(write_group, text="WriteFlash",
                           command=esp_func_calls.write_flash)
        button.grid(column=0, row=row_pos_write,
                    columnspan=2, sticky="EW", padx=3, pady=3)

        tk.Grid.columnconfigure(write_group, 0, weight=1)
        tk.Grid.columnconfigure(write_group, 1, weight=2)

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
