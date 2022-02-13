"""
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
"""

import sys
import os

import glob
from io import StringIO
import tkinter as tk
from tkinter import ttk

# import eef modules
from eef_modules.esptool_com import EsptoolCom

from eef_modules.io_redirection import StderrRedirection
from eef_modules.io_redirection import StdoutRedirection
from eef_modules.eef_config import EEFConfig

from eef_modules.esp_func_calls import EspFuncCalls
from eef_modules.public_gui_elements import PublicGUIElements

from eef_modules.frame_serial_monitor import SerialMonitorFrame

from eef_modules.label_frame_handler import LabelFrameHandler


ESP_PACKAGES = "./ESP_Packages"


class EspEasyFlasher:
    """TkInter App class EspEasyFlasher"""

    def __init__(self, master):
        self.file_list = []
        str_io = StringIO()
        esp_com = EsptoolCom()
        eef_config = EEFConfig(str_io, esp_com)
        base_path = eef_config.get_base_path()

        public_gui_elements = PublicGUIElements()

        str_io.write(f"os: {sys.platform}\n")
        if eef_config.is_pyinstaller():
            if sys.platform != "win32":
                path = os.path.sep.join(sys.argv[0].split(os.path.sep))
                dirname = os.path.dirname(path)
                os.chdir(dirname)
                str_io.write(f"{dirname}\n")
            else:
                icon_file = "./icon_256x256.png"
                icon_path = os.path.join(base_path, icon_file)
                root.iconphoto(False, tk.PhotoImage(file=icon_path))

        str_io.write(f"CWD: {os.getcwd()}\n")
        root_dir = os.getcwd()
        esp_com.root_dir = root_dir

        master.title("ESPEasyFlasher2.0")
        master.resizable(0, 0)

        frame = ttk.Frame(master)
        frame.pack()

        label_frames = LabelFrameHandler(frame, eef_config)
        esp_func_calls = EspFuncCalls(public_gui_elements, esp_com, label_frames)

        # Serial Com Port Group
        row_pos_frame = 0
        label_frames.set_pos_header_frame(row_pos_frame, esp_func_calls)

        # Write Flash Group
        row_pos_frame += 1
        file_list = EspEasyFlasher.get_file_list()
        label_frames.set_pos_write_frame(row_pos_frame, file_list, esp_func_calls)

        # Read Flash Group (optional)
        if eef_config.with_developer_mode():
            row_pos_frame += 1
            label_frames.set_pos_read_frame(row_pos_frame, esp_func_calls)

            row_pos_frame += 1
            label_frames.set_pos_erase_frame(row_pos_frame, esp_func_calls)

        # create Text box for Logging
        text_box = tk.Text(frame, wrap='word', height=11, width=80)

        # Serial Monitor
        if eef_config.with_serial_monitor():
            row_pos_frame += 1
            public_gui_elements.set_frame_serial_monitor(SerialMonitorFrame(frame, row_pos_frame, text_box,
                                                                            label_frames.get_com_port))

        # Textbox Logging
        row_pos_frame += 1

        text_box.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame, command=text_box.yview)
        scrollbar.grid(row=row_pos_frame, column=2, sticky='nsew')
        text_box['yscrollcommand'] = scrollbar.set
        public_gui_elements.set_text_box(text_box)

        # Progressbar
        row_pos_frame += 1
        progress_bar = ttk.Progressbar(frame, orient="horizontal", length=200, mode="determinate")
        progress_bar.grid(column=0, row=row_pos_frame, columnspan=2, sticky="EW", padx=5, pady=5)
        public_gui_elements.set_progress_bar(progress_bar)

        # create stdout and stderr redirection instances
        stdout_redirection = StdoutRedirection(public_gui_elements)
        stderr_redirection = StderrRedirection(public_gui_elements)

        public_gui_elements.set_stdout_redirection(stdout_redirection)

        # redirection of stdout and stderr
        sys.stdout = stdout_redirection
        sys.stderr = stderr_redirection

        # write config string
        text_box.insert(tk.END, str_io.getvalue())

        # scan com ports
        label_frames.com_port_scan()

    @staticmethod
    def get_file_list():
        """get file list for write combobox, depends on file extension,
        can be zip (ESPEasyFlasher Package)
        eef files with required bin files
        or only a bin for a ESP8266"""
        file_list = glob.glob("*.zip", root_dir=ESP_PACKAGES)
        if len(file_list) == 0:
            file_list = glob.glob("*.eef", root_dir=ESP_PACKAGES)
            if len(file_list) == 0:
                file_list = glob.glob("*.bin", root_dir=ESP_PACKAGES)
        return file_list


if __name__ == "__main__":
    root = tk.Tk()
    app = EspEasyFlasher(root)
    root.mainloop()
