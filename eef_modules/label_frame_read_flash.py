"""
  label_frame_read_flash.py is used by ESPEasyFlasher.py to create and handle the read Label Frame.
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

import tkinter as tk


# pylint: disable=too-few-public-methods
class ReadLabelFrame:
    """
    Class to create and handle the Read Label Frame
    """
    def __init__(self, frame, row_pos_frame, esp_func_calls) -> None:
        read_group = tk.LabelFrame(frame, text='ReadFlash')
        read_group.grid(column=0, row=row_pos_frame,
                              columnspan=3, sticky="EW", padx=5, pady=5)

        row_pos_read = 0
        label_read_flash = tk.Label(read_group, text="Flash write to: ")
        label_read_flash.grid(column=0, row=row_pos_read, sticky="W")

        default_text = tk.StringVar(read_group, value="filename_read_flash")
        self.__entry_file_name = tk.Entry(read_group, width=20, textvariable=default_text)
        self.__entry_file_name.grid(column=1, row=row_pos_read, sticky="EW")

        file_extension = tk.Label(read_group, text=".bin")
        file_extension.grid(column=2, row=row_pos_read, sticky="W")

        row_pos_read += 1
        read_btn = tk.Button(read_group, text="ReadFlash", command=esp_func_calls.read_flash)
        read_btn.grid(column=0, row=row_pos_read, columnspan=3, sticky="EW", padx=3, pady=3)

        tk.Grid.columnconfigure(read_group, 0, weight=1)
        tk.Grid.columnconfigure(read_group, 1, weight=2)
        tk.Grid.columnconfigure(read_group, 2, weight=1)

    def get_read_file_name(self):
        """get file name"""
        return self.__entry_file_name.get()
