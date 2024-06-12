"""
  ESPEasyFlasher.py is a Simple GUI for esptool.py by espressif
  (https://github.com/espressif/esptool)

  It is also written in Python and is using Tkinter as GUI framework.

  Targets:
    * Using should be simple, also for people without experience of command line tools
    * It can be easily configured by experienced people and user of the esptool.py
    * It can be used in two modes (Developer/User)
    * It is platform independent same as esptool.py

  Copyright (C) 2022  André Herrmann
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

from io import StringIO
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# import eef modules
from eef_modules.eef_esptool_com.esptool_com import EsptoolCom
from eef_modules.eef_helper.eef_config import EEFConfig
from eef_modules.eef_esptool_com.esp_func_calls import EspFuncCalls
from eef_modules.bottom_gui_elements import BottomGUIElements
from eef_modules.label_frame_handler import LabelFrameHandler

EEF_CONFIG = "./ESPEasyFlasherConfig.json"
EEF_LOGO_FILE = "./LogoEasyFlash.png"

# pylint: disable=too-few-public-methods
class EspEasyFlasher:
    """TkInter App class EspEasyFlasher"""
    def __init__(self, master):
        self.master = master
        self.file_list = []
        str_io = StringIO()
        esp_com = EsptoolCom()
        eef_config = EEFConfig(EEF_CONFIG, EEF_LOGO_FILE, str_io, esp_com)
        base_path = eef_config.get_base_path()

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
                master.iconphoto(False, tk.PhotoImage(file=icon_path))

        str_io.write(f"CWD: {os.getcwd()}\n")
        root_dir = os.getcwd()
        esp_com.root_dir = root_dir
        self.info = eef_config.get_info()

        # init "__init_gui_frame contains" as last one!
        # Because the method contains a redirection of stdout
        # If something goes wrong, errors will not be visible in terminal
        # in case it is not the last one!
        self.__init_gui_frame(eef_config, esp_com, str_io)

    def __init_gui_frame(self, eef_config, esp_com, str_io):
        """ creates the GUI ESPEasyFlasher2.0 """
        self.master.title("ESPEasyFlasher2.0")
        self.master.resizable(0, 0)

        frame = ttk.Frame(self.master)
        frame.pack()

        label_frames = LabelFrameHandler(frame, eef_config)
        bottom_gui_elements = BottomGUIElements(frame)
        esp_func_calls = EspFuncCalls(bottom_gui_elements, esp_com, label_frames)

        # Serial Com Port Group
        row_pos_frame = 0
        label_frames.set_pos_header_frame(row_pos_frame, esp_func_calls)

        # Write Flash Group
        row_pos_frame += 1
        label_frames.set_pos_write_frame(row_pos_frame, esp_func_calls)

        # Read Flash Group (optional)
        if eef_config.with_developer_mode():
            row_pos_frame += 1
            label_frames.set_pos_read_frame(row_pos_frame, esp_func_calls)

            row_pos_frame += 1
            label_frames.set_pos_erase_frame(row_pos_frame, esp_func_calls)

        # Serial Monitor
        if eef_config.with_serial_monitor():
            row_pos_frame += 1
            bottom_gui_elements.set_pos_serial_monitor_frame(row_pos_frame, label_frames.get_com_port)

        # Textbox Logging
        row_pos_frame += 1
        bottom_gui_elements.set_pos_text_box(row_pos_frame)

        # Progressbar
        row_pos_frame += 1
        bottom_gui_elements.set_pos_progress_bar(row_pos_frame)

        # redirect stdout and stderr to textbox
        bottom_gui_elements.redirect_stdout_to_textbox()

        # write config string
        bottom_gui_elements.append_text(str_io.getvalue())

        # scan com ports
        label_frames.com_port_scan()

    def get_info(self):
        """show EEF build info in dialog"""
        messagebox.showinfo("Info ESPEASYFLASHER 2.0", self.info)

    # def create_error_report(self):
    #     info = self.info

if __name__ == "__main__":
    root = tk.Tk()
    menu = tk.Menu(root)
    root.config(menu=menu)
    app = EspEasyFlasher(root)

    helpmenu = tk.Menu(menu)
    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label="Info", command=app.get_info)
#    helpmenu.add_command(label="Error Report", command=app.create_error_report)
    helpmenu.add_separator()
    helpmenu.add_command(label="Exit", command=root.quit)
    root.mainloop()
