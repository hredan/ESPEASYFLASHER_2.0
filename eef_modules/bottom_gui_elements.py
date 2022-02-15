"""
  bottom_gui_elements.py is used by ESPEasyFlasher.py to handle the frame Serial Monitor, the output text box with
  scrollbar and the progress bar in the bottom of GUI.
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

import sys
import tkinter as tk
from tkinter import ttk
from eef_modules.serial_monitor.frame_serial_monitor import SerialMonitorFrame
from eef_modules.eef_helper.io_redirection import StderrRedirection
from eef_modules.eef_helper.io_redirection import StdoutRedirection


# pylint: disable=too-many-instance-attributes
class BottomGUIElements:
    """
    BottomGUIElements handles the SerialMonitorFrame, Output Textbox with scrollbar and the progress bar
    """
    def __init__(self, frame) -> None:
        self.__frame = frame
        self.__progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
        self.__text_box = tk.Text(frame, wrap='word', height=11, width=80)
        self.__root_dir = None
        self.__frame_serial_monitor = SerialMonitorFrame(frame, self.__text_box)

    def set_pos_serial_monitor_frame(self, row_pos_frame, get_com_port):
        """ full initializing and positioning of serial monitor frame parts"""
        self.__frame_serial_monitor.set_positioning(row_pos_frame, get_com_port)

    def set_pos_text_box(self, row_pos_frame):
        """ full initializing and positioning of output text box"""
        self.__text_box.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW", padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.__frame, command=self.__text_box.yview)
        scrollbar.grid(row=row_pos_frame, column=2, sticky='nsew')
        self.__text_box['yscrollcommand'] = scrollbar.set

    def set_pos_progress_bar(self, row_pos_frame):
        """ full initializing and positioning of progress bar """
        self.__progress_bar.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW", padx=5, pady=5)

    def append_text(self, text):
        """ append text at the end of output text box """
        self.__text_box.insert(tk.END, text)

    def redirect_stdout_to_textbox(self):
        """ redirection of stdout and stderr to output text box"""
        # create stdout and stderr redirection instances
        stdout_redirection = StdoutRedirection(self.__text_box, self.__progress_bar)
        stderr_redirection = StderrRedirection(self.__text_box, self.__progress_bar)

        # redirection of stdout and stderr
        sys.stdout = stdout_redirection
        sys.stderr = stderr_redirection

    def set_root_dir(self, root_dir):
        """
        set root dir
        """
        self.__root_dir = root_dir

    def get_root_dir(self):
        """
        get root dir
        """
        return self.__root_dir
