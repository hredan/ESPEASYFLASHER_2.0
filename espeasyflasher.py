
'''
  ESPEasyFlasher.py is a Simple GUI for esptool.py by espressif
  (https://github.com/espressif/esptool)

  It is also written in Python and is using Tkinter as GUI framework.

  Targets:
    * Using should be simple, also for people without experience of command line tools
    * It can be easily configured by experienced people and user of the esptool.py
    * It can be used in two modes (Developer/User)
    * It is platform independent same as esptool.py

  Copyright (C) 2021  André Herrmann
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

import sys
import os
import shutil
import zipfile
import threading
import re
import json
import glob
from io import StringIO
import tkinter as tk
from tkinter import ttk
from serial.tools.list_ports import comports
from esptool_com import EsptoolCom
import serial_monitor as sm
from io_redirection import StderrRedirection
from io_redirection import StdoutRedirection


class EspEasyFlasher:
    """TkInter App class EspEasyFlasher"""

    def logo_file_exists(self):
        """check if logo file exists"""
        return_value = False
        filename = "./LogoEasyFlash.png"
        if os.path.exists(filename):
            self.logo_file_path = filename
            return_value = True
        elif self.check_meipass():
            self.logo_file_path = os.path.join(self.base_path, filename)
            return_value = True
        else:
            return_value = False
            self.str_io.write(
                f"Warning: Could not find '{filename}', using layout without logo!\n")

        return return_value

    def grid_without_logo(self, row_pos_frame):
        """set gird columnspan to 3 means without logo"""
        self.com_group.grid(column=0, row=row_pos_frame,
                            columnspan=3, sticky="EW", padx=5, pady=5)

    def __init__(self, master):
        self.developer_mode = True
        self.with_logo = True
        self.with_serial_monitor = True
        self.file_list = []
        self.str_io = StringIO()
        self.esp = EsptoolCom()

        self.serial_monitor = None

        self.str_io.write(f"os: {sys.platform}\n")
        if self.check_meipass():
            if sys.platform != "win32":
                path = os.path.sep.join(sys.argv[0].split(os.path.sep))
                dirname = os.path.dirname(path)
                os.chdir(dirname)
                self.str_io.write(f"{dirname}\n")
            else:
                icon_file = "./icon_256x256.png"
                icon_path = os.path.join(self.base_path, icon_file)
                root.iconphoto(False, tk.PhotoImage(file=icon_path))

        self.str_io.write(f"CWD: {os.getcwd()}\n")
        self.root_dir = os.getcwd()
        self.esp.root_dir = self.root_dir

        # read config from json file
        self.read_config()

        master.title("ESPEasyFlasher2.0")
        master.resizable(0, 0)

        frame = ttk.Frame(master)
        frame.pack()

        row_pos_frame = 0
        self.com_group = tk.LabelFrame(frame, text='Serial Com Port')

        if self.with_logo:
            if self.logo_file_exists():
                self.com_group.grid(column=0, row=row_pos_frame,
                                    sticky="EW", padx=5, pady=5)
                self.logo = tk.PhotoImage(file=self.logo_file_path)
                self.label_logo = tk.Label(frame, image=self.logo)
                self.label_logo.grid(column=1, row=row_pos_frame,
                                    columnspan=2, sticky="EW")
            else:
                self.grid_without_logo(row_pos_frame)
        else:
            self.grid_without_logo(row_pos_frame)

        # Com Port
        row_pos_com = 0
        self.label_com_port = tk.Label(self.com_group, text="Com Port: ")
        self.label_com_port.grid(column=0, row=row_pos_com, sticky="W")

        self.combo_com_port = ttk.Combobox(self.com_group)
        self.combo_com_port.grid(column=1, row=row_pos_com,
                               sticky="WE", padx=3, pady=3)

        row_pos_com += 1
        self.com_btn_frame = tk.Frame(self.com_group)
        self.com_btn_frame.grid(column=0, row=row_pos_com,
                              columnspan=2, sticky="EW")

        if self.esp_info:
            self.com_refresh_btn = tk.Button(
                self.com_btn_frame, text="Scan", command=self.com_port_scan)
            self.com_refresh_btn.grid(
                column=0, row=0, sticky="EW", padx=3, pady=3)

            self.esp_info = tk.Button(
                self.com_btn_frame, text="ESP Info", command=self.get_esp_info)
            self.esp_info.grid(column=1, row=0, sticky="EW", padx=3, pady=3)
        else:
            self.com_refresh_btn = tk.Button(
                self.com_btn_frame, text="Scan", command=self.com_port_scan)
            self.com_refresh_btn.grid(
                column=0, row=0, columnspan=2, sticky="EW", padx=3, pady=3)

        tk.Grid.columnconfigure(self.com_group, 0, weight=1)
        tk.Grid.columnconfigure(self.com_group, 1, weight=2)

        tk.Grid.columnconfigure(self.com_btn_frame, 0, weight=1)
        tk.Grid.columnconfigure(self.com_btn_frame, 1, weight=1)

        # write Group
        row_pos_frame += 1
        self.write_group = tk.LabelFrame(frame, text='WriteFlash')
        self.write_group.grid(column=0, row=row_pos_frame,
                             columnspan=3, sticky="EW", padx=5, pady=5)

        row_pos_write = 0
        self.label_write_flash = tk.Label(self.write_group, text="bin file: ")
        self.label_write_flash.grid(column=0, row=row_pos_write, sticky="W")

        self.combo_write_flash = ttk.Combobox(self.write_group)
        self.file_list = self.get_file_list()
        self.set_file_list_combo_write(self.file_list)
        self.combo_write_flash.grid(column=1, row=row_pos_write,
                                sticky="EW", padx=3, pady=3)

        row_pos_write += 1
        self.button = tk.Button(
            self.write_group, text="WriteFlash", command=self.write_flash)
        self.button.grid(column=0, row=row_pos_write,
                         columnspan=2, sticky="EW", padx=3, pady=3)

        tk.Grid.columnconfigure(self.write_group, 0, weight=1)
        tk.Grid.columnconfigure(self.write_group, 1, weight=2)

        # read Group
        if self.developer_mode:
            row_pos_frame += 1
            self.read_group = tk.LabelFrame(frame, text='ReadFlash')
            self.read_group.grid(column=0, row=row_pos_frame,
                                columnspan=3, sticky="EW", padx=5, pady=5)

            row_pos_read = 0
            self.label_read_flash = tk.Label(
                self.read_group, text="Flash write to: ")
            self.label_read_flash.grid(column=0, row=row_pos_read, sticky="W")

            default_text = tk.StringVar(
                self.read_group, value="filename_read_flash")
            self.entry_file_name = tk.Entry(
                self.read_group, width=20, textvariable=default_text)
            self.entry_file_name.grid(column=1, row=row_pos_read, sticky="EW")

            self.file_extension = tk.Label(self.read_group, text=".bin")
            self.file_extension.grid(column=2, row=row_pos_read, sticky="W")

            row_pos_read += 1
            self.read_btn = tk.Button(
                self.read_group, text="ReadFlash", command=self.read_flash)
            self.read_btn.grid(column=0, row=row_pos_read,
                              columnspan=3, sticky="EW", padx=3, pady=3)

            tk.Grid.columnconfigure(self.read_group, 0, weight=1)
            tk.Grid.columnconfigure(self.read_group, 1, weight=2)
            tk.Grid.columnconfigure(self.read_group, 2, weight=1)

            row_pos_frame += 1
            self.erase_group = tk.LabelFrame(frame, text='EraseFlash')
            self.erase_group.grid(column=0, row=row_pos_frame,
                                 columnspan=3, sticky="EW", padx=5, pady=5)

            row_pos_erase = 0
            self.read_btn = tk.Button(
                self.erase_group, text="EraseFlash", command=self.erase_flash)
            self.read_btn.grid(column=0, row=row_pos_erase,
                              sticky="EW", padx=3, pady=3)

            tk.Grid.columnconfigure(self.erase_group, 0, weight=1)
        # Serial Monitor
        if self.with_serial_monitor:
            row_pos_frame += 1
            self.status_serial_monitor = False
            self.serial_monitor_frame = tk.Frame(frame)
            self.serial_monitor_frame.grid(
                column=0, row=row_pos_frame, columnspan=2, sticky="EW")

            self.label_serial_monitor = tk.Label(
                self.serial_monitor_frame, text="Serial Monitor: ")
            self.label_serial_monitor.grid(column=0, row=0, sticky="W")

            self.serial_monitor_btn_on_off = tk.Button(
                self.serial_monitor_frame, text="On", command=self.serial_monitor_switch)
            self.serial_monitor_btn_on_off.grid(
                column=1, row=0, sticky="EW", padx=3, pady=3)

            self.esp_reset_btn = tk.Button(self.serial_monitor_frame,
                        text="ESP Reset", state=tk.DISABLED, command=self.esp_reset)
            self.esp_reset_btn.grid(column=2, row=0, sticky="EW", padx=3, pady=3)

        # Textbox Logging
        row_pos_frame += 1
        self.text_box = tk.Text(frame, wrap='word', height=11, width=80)
        self.text_box.grid(column=0, row=row_pos_frame,
                           columnspan=2, sticky="EW", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame, command=self.text_box.yview)
        scrollbar.grid(row=row_pos_frame, column=2, sticky='nsew')
        self.text_box['yscrollcommand'] = scrollbar.set

        if self.with_serial_monitor:
            self.serial_monitor = sm.SerialMonitor(self.text_box)

        # Progressbar
        row_pos_frame += 1
        self.progress = ttk.Progressbar(frame, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress.grid(column=0, row=row_pos_frame,
                           columnspan=2, sticky="EW", padx=5, pady=5)

        self.stdout_redirection = StdoutRedirection(self.text_box, self.progress)
        self.stderr_redirection = StderrRedirection(self.text_box, self.progress)
        sys.stdout = self.stdout_redirection
        sys.stderr = self.stderr_redirection

        # write config string
        self.text_box.insert(tk.END, self.str_io.getvalue())

        # scan com ports
        self.com_port_scan()

    def esp_reset(self):
        """ trigger esp reset via RTS pins"""
        if (self.status_serial_monitor and self.serial_monitor):
            print("### Hard Reset via RTS pin ###")
            self.serial_monitor.esp_reset()

    def serial_monitor_switch(self):
        """ enable/disable Serial Monitor"""
        com_port = self.combo_com_port.get()
        if self.status_serial_monitor:
            self.status_serial_monitor = False
            self.serial_monitor_btn_on_off.config(text="On", bg="grey")
            self.esp_reset_btn.config(state=tk.DISABLED)
            if self.serial_monitor:
                self.serial_monitor.stop_thread()
        else:
            self.status_serial_monitor = True
            self.serial_monitor_btn_on_off.config(text="Off", bg="green")
            self.esp_reset_btn.config(state=tk.NORMAL)
            if self.serial_monitor:
                self.serial_monitor.start_thread(com_port)

    def base_thread(self, target_method, info_text, set_progressbar=False,
                   second_arg=None, third_arg=None):
        """base thread"""
        os.chdir(self.root_dir)
        print(f"Info: CWD {os.getcwd()}")
        if set_progressbar:
            self.progress["value"] = 0
            self.progress["maximum"] = 100

        # Disable Serial Monitor if enabled
        if self.status_serial_monitor:
            self.serial_monitor_switch()
        print(info_text)
        com_port = self.combo_com_port.get()
        if com_port == "":
            print("Error: select a Serial Com Port before you can start read flash!")
        else:
            if third_arg:
                thread = threading.Thread(target=target_method, args=(
                    com_port, second_arg, third_arg, ))
            elif second_arg:
                thread = threading.Thread(target=target_method,
                                     args=(com_port, second_arg, ))
            else:
                thread = threading.Thread(target=target_method, args=(com_port,))
            thread.start()

    def esp_info_callback(self):
        """ Callback function for esp threads"""
        print(f"Detected ESP of type: {self.stdout_redirection.esp_type}, " +
              f"with Flash Size of: {self.stdout_redirection.esp_flash_size}")
        file_list = []
        if self.stdout_redirection.esp_type:

            for entry in self.file_list:
                if re.match(f"^{self.stdout_redirection.esp_type}", entry, re.IGNORECASE):
                    file_list.append(entry)

            if len(file_list) > 0:
                self.set_file_list_combo_write(file_list)
                print(f"Filter {self.stdout_redirection.esp_type} files")
            else:
                print(
                    f"[War] Could not find entries for {self.stdout_redirection.esp_type}")
                self.set_file_list_combo_write(self.file_list)

    def get_esp_info(self):
        """ESP Info request"""
        self.stdout_redirection.esp_type = None
        self.stdout_redirection.esp_flash_size = None
        self.base_thread(self.esp.esptool_esp_info,
                        "### ESP INFO ###", False, self.esp_info_callback)

    def erase_flash(self):
        """erase ESP flash"""
        self.base_thread(self.esp.esptool_erase_flash, "### Erase Flash ###")

    def write_flash(self):
        """ write data to ESP flash"""
        filename = self.combo_write_flash.get()
        if filename == "":
            print("Error: before you can write to flash, select a firmware.bin file")
        else:
            file_name, file_extension = os.path.splitext(filename)
            if file_extension == ".eef":
                content_path = f"{self.root_dir}/ESP_Packages"
                eef_path = f"{content_path}/{filename}"
                print(f"Info: eef file path: {eef_path}")
                command = self.read_eef_file(eef_path)
                self.base_thread(self.esp.esptool_write_eef,
                                "### Write Flash ###", True, command, content_path)
            elif file_extension == ".zip":
                extract_path = f"{self.root_dir}/ESP_Packages/Extracted"
                zip_path = f"{self.root_dir}/ESP_Packages/{filename}"
                eef_path = f"{self.root_dir}/ESP_Packages/Extracted/{file_name}.eef"
                # make dir, if exist clear content of dir
                if os.path.exists(extract_path):
                    shutil.rmtree(extract_path)
                else:
                    os.mkdir(extract_path)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                if os.path.exists(eef_path):
                    print(f"Info: eef file path: {eef_path}")
                    command = self.read_eef_file(eef_path)
                    self.base_thread(
                        self.esp.esptool_write_eef, "### Write Flash ###",
                        True, command, extract_path)
                else:
                    print(
                        f"Error: WriteFlash->could not find eef file, expected {eef_path}")

            else:
                self.base_thread(self.esp.esptool_write_flash,
                                "### Write Flash ###", True, filename)

    def read_flash(self):
        """ read ESP flash"""
        filename = self.entry_file_name.get()
        if filename == "":
            print("Error: before you can read flash, define a filename")
        else:
            filename = filename + ".bin"
            self.base_thread(self.esp.esptool_read_flash,
                            "### Read Flash ###", True, filename)

    def read_eef_file(self, filename):
        """read esptool parameter settings from eef file"""
        self.str_io.write("### read eef file ###\n")
        return_value = ""
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                return_value = data['command']

        except EnvironmentError as err:
            self.str_io.writelines(
                f"Error could not read eef file {filename}: {err}\n")
        return return_value

    def get_file_list(self):
        """get file list for write combobox, depends on file extension,
        can be zip (ESPEasyFlasher Package)
        eef files with required bin files
        or only a bin for a ESP8266"""
        file_list = glob.glob("*.zip", root_dir="./ESP_Packages")
        if len(file_list) == 0:
            file_list = glob.glob("*.eef", root_dir="./ESP_Packages")
            if len(file_list) == 0:
                file_list = glob.glob("*.bin", root_dir="./ESP_Packages")
        return file_list

    def set_file_list_combo_write(self, file_list):
        """set file list for combobox write flash"""
        self.combo_write_flash["values"] = file_list
        if len(file_list) > 0:
            self.combo_write_flash.current(0)

    def com_port_scan(self):
        """scan for serial usb com port"""
        com_info = self.get_com_info()
        if len(com_info["comlist"]) > 0:
            self.combo_com_port["values"] = com_info["comlist"]

            if com_info["defaultCom"] != "":
                self.combo_com_port.current(
                    com_info["comlist"].index(com_info["defaultCom"]))
            else:
                self.combo_com_port.current(0)

    def get_com_info(self):
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

    def read_config(self):
        self.str_io.write("### Read Config ###\n")
        try:
            with open('ESPEasyFlasherConfig.json') as json_file:
                data = json.load(json_file)

                self.with_logo = data['logo']
                self.str_io.writelines(f"enable logo: {data['logo']}\n")

                self.developer_mode = data['devMode']
                self.str_io.writelines(f"dev mode is: {data['devMode']}\n")

                self.with_serial_monitor = data['serialMonitor']
                self.str_io.writelines(
                    f"serial monitor: {data['serialMonitor']}\n")

                self.esp_info = data['espInfo']
                self.str_io.writelines(f"esp info: {self.esp_info}\n")

                self.esp.baud_rate = data['baudRate']
                self.str_io.write(f"set baud rate to: {data['baudRate']}\n")

                self.esp.read_start = data['readStart']
                self.str_io.write(f"set read start to: {data['readStart']}\n")

                self.esp.read_size = data['readSize']
                self.str_io.write(f"set read size to: {data['readSize']}\n")

                self.esp.write_start = data['writeStart']
                self.str_io.write(
                    f"set write start to: {data['writeStart']}\n")

        except EnvironmentError as err:
            self.str_io.writelines(
                f"Error could not read config, default values will be used: {err}\n")

    def check_meipass(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        return_value = False
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            self.base_path = sys._MEIPASS
            return_value = True
        except Exception:
            self.base_path = os.path.abspath(".")
            return_value = False

        return return_value


if __name__ == "__main__":
    root = tk.Tk()
    app = EspEasyFlasher(root)
    root.mainloop()
