"""
  public_gui_elements.py is used by ESPEasyFlasher.py to handle GUI elemtens
  wish are used by other instances.
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


# pylint: disable=too-many-instance-attributes
class PublicGUIElements:
    """
    PublicGUIElements is a Helper Class to share GUI instances
    """
    def __init__(self) -> None:
        self.__progress_bar = None
        self.__text_box = None
        self.__stdout_redirection = None
        self.__root_dir = None
        self.__label_frame_write_flash = None
        self.__label_frame_serial = None
        self.__label_frame_read_flash = None
        self.__label_frame_erase_flash = None
        self.__frame_serial_monitor = None

    def set_progress_bar(self, progress_bar):
        """
        set the progress bar
        """
        self.__progress_bar = progress_bar

    def get_progress_bar(self):
        """
        get the progress bar
        """
        return self.__progress_bar

    def set_text_box(self, text_box):
        """
        set text box
        """
        self.__text_box = text_box

    def get_text_box(self):
        """
        get text box
        """
        return self.__text_box

    def set_stdout_redirection(self, stdout_redirection):
        """
        set stdout redirection
        """
        self.__stdout_redirection = stdout_redirection

    def get_stdout_redirection(self):
        """
        get stdout redirection
        """
        return self.__stdout_redirection

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

    def set_label_frame_write(self, label_frame_write):
        """
        set write_group
        """
        self.__label_frame_write_flash = label_frame_write

    def get_label_frame_write(self):
        """
        get write group
        """
        return self.__label_frame_write_flash

    def set_label_frame_serial_com(self, label_frame_serial_com):
        """
        set serial_com_group
        """
        self.__label_frame_serial = label_frame_serial_com

    def get_label_frame_serial_com(self):
        """
        get serial_com_group
        """
        return self.__label_frame_serial

    def set_label_frame_read(self, label_frame_read):
        """
        set label frame read flash
        """
        self.__label_frame_read_flash = label_frame_read

    def get_label_frame_read(self):
        """
        get label frame read flash
        """
        return self.__label_frame_read_flash

    def set_label_frame_erase(self, label_frame_erase):
        """
        set label frame erase flash
        """
        self.__label_frame_erase_flash = label_frame_erase

    def get_label_frame_erase(self):
        """
        get label frame erase flash
        """
        return self.__label_frame_erase_flash

    def set_frame_serial_monitor(self, frame_serial_monitor):
        """
        set frame serial monitor
        """
        self.__frame_serial_monitor = frame_serial_monitor

    def get_frame_serial_monitor(self):
        """
        get frame serial monitor
        """
        return self.__frame_serial_monitor
