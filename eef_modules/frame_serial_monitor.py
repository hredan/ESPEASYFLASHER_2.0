'''
  frame_serial_monitor.py is used by ESPEasyFlasher.py to create and handle Serial Monitor Frame.
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

from eef_modules.serial_monitor import SerialMonitor

class SerialMonitorFrame:
    """
    Class to create and handle the Serial Monitor Frame
    """
    def __init__(self, frame, row_pos_frame, text_box, label_frame_serial_com) -> None:
        self.__status_serial_monitor = False
        self.__serial_monitor_thread = SerialMonitor(text_box)
        self.__label_frame_serial_com = label_frame_serial_com

        serial_monitor_frame = tk.Frame(frame)
        serial_monitor_frame.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW")

        label_serial_monitor = tk.Label(serial_monitor_frame, text="Serial Monitor: ")
        label_serial_monitor.grid(column=0, row=0, sticky="W")

        self.__serial_monitor_btn_on_off = tk.Button(serial_monitor_frame, text="On",
                                                        command=self.serial_monitor_switch)
        self.__serial_monitor_btn_on_off.grid(column=1, row=0, sticky="EW", padx=3, pady=3)

        self.__esp_reset_btn = tk.Button(serial_monitor_frame, text="ESP Reset",
                                            state=tk.DISABLED, command=self.esp_reset)
        self.__esp_reset_btn.grid(column=2, row=0, sticky="EW", padx=3, pady=3)

    def esp_reset(self):
        """ trigger esp reset via RTS pins"""
        if (self.__status_serial_monitor and self.__serial_monitor_thread):
            print("### Hard Reset via RTS pin ###")
            self.__serial_monitor_thread.esp_reset()

    def serial_monitor_switch(self):
        """ enable/disable Serial Monitor"""
        com_port = self.__label_frame_serial_com.get_com_port()
        if self.__status_serial_monitor:
            self.__status_serial_monitor = False
            self.__serial_monitor_btn_on_off.config(text="On", bg="grey")
            self.__esp_reset_btn.config(state=tk.DISABLED)
            if self.__serial_monitor_thread:
                self.__serial_monitor_thread.stop_thread()
        else:
            self.__status_serial_monitor = True
            self.__serial_monitor_btn_on_off.config(text="Off", bg="green")
            self.__esp_reset_btn.config(state=tk.NORMAL)
            if self.__serial_monitor_thread:
                self.__serial_monitor_thread.start_thread(com_port)
