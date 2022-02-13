"""
  serial_com.py is used by ESPEasyFlasher.py to create and handle the
  Label Frame Serial Com (contains selection of serial com port, logo, and ESP Info).
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

import tkinter as tk
from tkinter import ttk

from serial.tools.list_ports import comports


class SerialComLabelFrame(tk.LabelFrame):
    """
    SerialComLabelFrame (header frame) contains section of serial com port, logo, and ESP Info
    """

    def __init__(self, frame, label_str, eef_config):
        super().__init__(frame, text=label_str)
        # keep private reference
        self.__eef_config = eef_config
        self.__frame = frame

        self.__combo_com_port = ttk.Combobox(self)

    def set_positioning(self, row_pos_frame, esp_func_calls):
        """ define the positions from GUI elements in header frame """
        if self.__eef_config.with_logo():
            # with logo
            logo = tk.PhotoImage(file=self.__eef_config.get_logo_file_path())
            label_logo = tk.Label(self.__frame, image=logo)
            self.grid(column=0, row=row_pos_frame, sticky="EW", padx=5, pady=5)
            label_logo.grid(column=1, row=row_pos_frame, columnspan=2, sticky="EW")
        else:
            # without logo use columnspan = 3
            self.grid(column=0, row=row_pos_frame, columnspan=3, sticky="EW", padx=5, pady=5)

        # Position of comport label and combo box
        row_pos_com = 0
        label_com_port = tk.Label(self, text="Com Port: ")
        label_com_port.grid(column=0, row=row_pos_com, sticky="W")
        self.__combo_com_port.grid(column=1, row=row_pos_com, sticky="WE", padx=3, pady=3)

        # Postion of buttons Scan and ESP Info, vision of ESP Info depends on esp config
        row_pos_com += 1

        # create button frame with buttons Scan and ESP Info
        com_btn_frame = tk.Frame(self)
        com_btn_frame.grid(column=0, row=row_pos_com, columnspan=2, sticky="EW")
        com_refresh_btn = tk.Button(com_btn_frame, text="Scan", command=self.com_port_scan)
        if self.__eef_config.with_esp_info():
            com_refresh_btn.grid(column=0, row=0, sticky="EW", padx=3, pady=3)

            esp_info = tk.Button(com_btn_frame, text="ESP Info", command=esp_func_calls.get_esp_info)
            esp_info.grid(column=1, row=0, sticky="EW", padx=3, pady=3)
        else:
            com_refresh_btn.grid(column=0, row=0, columnspan=2, sticky="EW", padx=3, pady=3)

        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 1, weight=2)

        tk.Grid.columnconfigure(com_btn_frame, 0, weight=1)
        tk.Grid.columnconfigure(com_btn_frame, 1, weight=1)

    def com_port_scan(self):
        """scan for serial usb com port"""
        com_info = self.__get_com_info()
        if len(com_info["comlist"]) > 0:
            self.__combo_com_port["values"] = com_info["comlist"]

            if com_info["defaultCom"] != "":
                self.__combo_com_port.current(
                    com_info["comlist"].index(com_info["defaultCom"]))
            else:
                self.__combo_com_port.current(0)

    def get_com_port(self):
        """get com port name"""
        return self.__combo_com_port.get()

    @classmethod
    def __get_com_info(cls):
        """ get comports by serial.tools.list_ports
            and returns a list of usb com ports and the first usb com port as default
        """
        print("### Com Port Scan ###")
        usb_com_list = []
        default_com = ""

        com_ports = comports()
        print("Number of Com Ports: " + str(len(com_ports)))
        if len(com_ports) > 0:
            default_com = com_ports[0].device

        is_found_usb_serial_com_port = False
        for com in com_ports:
            # print(com.name)
            print("*" + com.description)
            usb_com_list.append(com.device)
            if com.description.lower().find("usb") != -1:
                default_com = com.device
                print("Found: "+default_com)
                is_found_usb_serial_com_port = True

        if not is_found_usb_serial_com_port:
            print(
                "Warning: could not find a usb-serial device, connect your device and scan again!")

        return {"comlist": usb_com_list, "defaultCom": default_com}
