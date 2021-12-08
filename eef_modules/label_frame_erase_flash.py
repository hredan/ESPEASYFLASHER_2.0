'''
  label_frame_erase_flash.py is used by ESPEasyFlasher.py to create and handle the Erase Label Frame.
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

class EraseLabelFrame:
    """
    Class to create and handle the Erase Label Frame
    """
    def __init__(self, frame, row_pos_frame, esp_func_calls) -> None:
        erase_group = tk.LabelFrame(frame, text='EraseFlash')
        erase_group.grid(column=0, row=row_pos_frame,
                                columnspan=3, sticky="EW", padx=5, pady=5)

        row_pos_erase = 0
        read_btn = tk.Button(erase_group, text="EraseFlash", command=esp_func_calls.erase_flash)
        read_btn.grid(column=0, row=row_pos_erase, sticky="EW", padx=3, pady=3)

        tk.Grid.columnconfigure(erase_group, 0, weight=1)