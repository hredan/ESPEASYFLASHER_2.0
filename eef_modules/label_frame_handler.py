"""
label_frames handels the
"""
from eef_modules.label_frames.serial_com import SerialComLabelFrame
from eef_modules.label_frames.write_flash import WriteLabelFrame
from eef_modules.label_frames.read_flash import ReadLabelFrame
from eef_modules.label_frames.erase_flash import EraseLabelFrame


class LabelFrameHandler:
    def __init__(self):
        self.__header_frame = None
        self.__write_frame = None
        self.__read_frame = None
        self.__erase_frame = None

    def create_header_frame(self, frame, row_pos_frame, eef_config, esp_func_calls):
        self.__header_frame = SerialComLabelFrame(frame, row_pos_frame, eef_config, esp_func_calls)

    def create_write_frame(self, frame, row_pos_frame, file_list, esp_func_calls):
        self.__write_frame = WriteLabelFrame(frame, row_pos_frame, file_list, esp_func_calls)

    def create_read_frame(self, frame, row_pos_frame, esp_func_calls):
        self.__read_frame = ReadLabelFrame(frame, row_pos_frame, esp_func_calls)

    def create_erase_frame(self, frame, row_pos_frame, esp_func_calls):
        self.__erase_frame = EraseLabelFrame(frame, row_pos_frame, esp_func_calls)

    def get_com_port(self):
        if self.__header_frame:
            return self.__header_frame.get_com_port()

    def com_port_scan(self):
        if self.__header_frame:
            return self.__header_frame.com_port_scan()

    def get_file_list_combo_write(self):
        return self.__write_frame.get_file_list_combo_write()

    def set_file_list_combo_write(self, file_list):
        self.__write_frame.set_file_list_combo_write(file_list)

    def get_filename_write(self):
        return self.__write_frame.get_file_name()

    def get_read_file_name(self):
        return self.__read_frame.get_read_file_name()
