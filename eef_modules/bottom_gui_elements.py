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


class BottomGUIElements:
    """
    BottomGUIElements handles the SerialMonitorFrame, Output Textbox with scrollbar and the progress bar
    """
    def __init__(self, frame) -> None:
        self.__frame = frame
        self.__progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
        self.__text_box = tk.Text(frame, wrap='word', height=11, width=80)
        self.__serial_send_frame = ttk.Frame(frame)
        self.__label_serial_command = ttk.Label(self.__serial_send_frame, text="Serial Command:")
        self.__entry_serial_command = ttk.Entry(self.__serial_send_frame)
        self.__serial_send_button = ttk.Button(self.__serial_send_frame, text="Send",
                                               command=self.__send_serial_command)
        self.__serial_command_history = []
        self.__serial_history_index = None
        self.__serial_history_unsent_text = ""
        self.__root_dir = None
        self.__frame_serial_monitor = SerialMonitorFrame(frame, self.__text_box)
        self.__show_serial_send_controls = True
        self.stdout_redirection = None

    def set_pos_serial_monitor_frame(self, row_pos_frame, get_com_port, show_send_controls=True):
        """ full initializing and positioning of serial monitor frame parts"""
        self.__show_serial_send_controls = show_send_controls
        self.__frame_serial_monitor.set_positioning(row_pos_frame, get_com_port)

    def set_pos_text_box(self, row_pos_frame):
        """ full initializing and positioning of output text box"""
        self.__text_box.grid(column=0, row=row_pos_frame, columnspan=2, sticky="NSEW", padx=5, pady=5)
        scrollbar = ttk.Scrollbar(self.__frame, command=self.__text_box.yview)
        scrollbar.grid(row=row_pos_frame, column=2, sticky='NS')
        self.__text_box['yscrollcommand'] = scrollbar.set

    def set_pos_progress_bar(self, row_pos_frame):
        """ full initializing and positioning of progress bar """
        self.__progress_bar.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW", padx=5, pady=5)

    def set_pos_serial_send_controls(self, row_pos_frame):
        """show command input and send button for serial monitor"""
        if not self.__show_serial_send_controls:
            return

        self.__serial_send_frame.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW", padx=5, pady=(0, 5))
        self.__serial_send_frame.columnconfigure(1, weight=1)

        self.__label_serial_command.grid(column=0, row=0, sticky="W", padx=(0, 3))
        self.__entry_serial_command.grid(column=1, row=0, sticky="EW", padx=3)
        self.__serial_send_button.grid(column=2, row=0, sticky="EW", padx=(3, 0))
        self.__entry_serial_command.bind("<Return>", self.__send_serial_command)
        self.__entry_serial_command.bind("<Up>", self.__show_previous_serial_command)
        self.__entry_serial_command.bind("<Down>", self.__show_next_serial_command)

    def append_text(self, text):
        """ append text at the end of output text box """
        self.__text_box.insert(tk.END, text)

    def redirect_stdout_to_textbox(self):
        """ redirection of stdout and stderr to output text box"""
        # create stdout and stderr redirection instances
        self.stdout_redirection = StdoutRedirection(self.__text_box, self.__progress_bar)
        stderr_redirection = StderrRedirection(self.__text_box, self.__progress_bar)

        # redirection of stdout and stderr
        sys.stdout = self.stdout_redirection
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

    def disable_serial_monitor(self):
        """
        disable serial monitor, if active
        """
        self.__frame_serial_monitor.disable_serial_monitor()

    def __send_serial_command(self, event=None):
        """send command from GUI entry field to serial interface"""
        del event
        command = self.__entry_serial_command.get().strip()
        if self.__frame_serial_monitor.send_serial_command(command):
            if command:
                self.__serial_command_history.append(command)
            self.__serial_history_index = None
            self.__serial_history_unsent_text = ""
            self.__entry_serial_command.delete(0, tk.END)

    def __show_previous_serial_command(self, event=None):
        """show previous command from history in entry field"""
        del event
        if not self.__serial_command_history:
            return "break"

        if self.__serial_history_index is None:
            self.__serial_history_unsent_text = self.__entry_serial_command.get()
            self.__serial_history_index = len(self.__serial_command_history) - 1
        elif self.__serial_history_index > 0:
            self.__serial_history_index -= 1

        self.__set_serial_command_entry(self.__serial_command_history[self.__serial_history_index])
        return "break"

    def __show_next_serial_command(self, event=None):
        """show next command from history in entry field"""
        del event
        if self.__serial_history_index is None:
            return "break"

        if self.__serial_history_index < len(self.__serial_command_history) - 1:
            self.__serial_history_index += 1
            self.__set_serial_command_entry(self.__serial_command_history[self.__serial_history_index])
        else:
            self.__serial_history_index = None
            self.__set_serial_command_entry(self.__serial_history_unsent_text)
        return "break"

    def __set_serial_command_entry(self, text):
        """replace full serial command entry content"""
        self.__entry_serial_command.delete(0, tk.END)
        self.__entry_serial_command.insert(0, text)
