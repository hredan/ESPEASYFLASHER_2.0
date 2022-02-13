"""
  label_frame_handler.py is used by ESPEasyFlasher.py to handle label frame GUI elemtens
  wish are used by other instances.
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
from eef_modules.label_frames.serial_com import SerialComLabelFrame
from eef_modules.label_frames.write_flash import WriteLabelFrame
from eef_modules.label_frames.read_flash import ReadLabelFrame
from eef_modules.label_frames.erase_flash import EraseLabelFrame


class LabelFrameHandler:
    """ the class LabelFrame Handler managed the Labelframes:
    SerialComLabelFrame (header_frame)

    """
    def __init__(self, frame, eef_config):

        self.__header_frame = SerialComLabelFrame(frame, eef_config)
        self.__write_frame = WriteLabelFrame(frame)
        self.__read_frame = ReadLabelFrame(frame)
        self.__erase_frame = EraseLabelFrame(frame)

    def set_pos_header_frame(self, row_pos_frame, esp_func_calls):
        """ init header frame with all parts and grid positions"""
        self.__header_frame.set_positioning(row_pos_frame, esp_func_calls)

    def set_pos_write_frame(self, row_pos_frame, file_list, esp_func_calls):
        """ init write frame """
        self.__write_frame.set_positioning(row_pos_frame, file_list, esp_func_calls)

    def set_pos_read_frame(self, row_pos_frame, esp_func_calls):
        """ init read frame """
        self.__read_frame.set_positioning(row_pos_frame, esp_func_calls)

    def set_pos_erase_frame(self, row_pos_frame, esp_func_calls):
        """ init erase frame """
        self.__erase_frame.set_positioning(row_pos_frame, esp_func_calls)

    def get_com_port(self):
        """ get com port from header frame"""
        return self.__header_frame.get_com_port()

    def com_port_scan(self):
        """ start com port scan"""
        return self.__header_frame.com_port_scan()

    def get_file_list_combo_write(self):
        """ get file list from combobox of write frame """
        return self.__write_frame.get_file_list_combo_write()

    def set_file_list_combo_write(self, file_list):
        """ set file list of combo box from write frame """
        self.__write_frame.set_file_list_combo_write(file_list)

    def get_filename_write(self):
        """ get filename entry of combobox from write frame """
        return self.__write_frame.get_file_name()

    def get_read_file_name(self):
        """ get filename entry of read frame """
        return self.__read_frame.get_read_file_name()
