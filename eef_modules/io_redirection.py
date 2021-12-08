'''
  io_redirection.py is used by ESPEasyFlasher.py to redirect and filter
  the stdout and stderr to the TK text_area.
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
import re

class IORedirection:
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self, public_gui_elements):
        self.text_area = public_gui_elements.get_text_box()
        self.progress_bar = public_gui_elements.get_progress_bar()
        self.text_area.tag_config("error", foreground="red")

    def flush(self):
        """dummy flush needed for IO"""

    @staticmethod
    def isatty():
        """dummy isatty needed for IO"""
        return False


class StderrRedirection(IORedirection):
    '''A class for redirecting stderr to this Text widget.'''
    def write(self, stderr_text_input):
        """
        write method, filtered the Stderr and adept the text before insert to the text_area

        Parameters:
        stderr_text_input (str): raw stderr input
        """
        self.text_area.insert(tk.END, stderr_text_input, "error")
        self.text_area.see(tk.END)



class StdoutRedirection(IORedirection):
    '''A class for redirecting stdout to this Text widget.'''
    esp_type = None
    esp_flash_size = None

    def normal_output(self, text_area_output):
        """
        standard method to insert text to text_area

        Parameters:
        input (str): text input
        """
        self.text_area.insert(tk.END, text_area_output)
        self.text_area.see(tk.END)

    def write(self, stdout_text_input):
        """
        write method, filtered the Stdout and adept the text before insert to the text_area

        Parameters:
        stdout_text_input (str): raw stdout input
        """
        read_match = re.match(r"^(\d+ \(\d+ %\)).*", stdout_text_input)
        write_match = re.match(r"^(Writing .+\((\d+) %\)).*", stdout_text_input)

        esp_type_match = re.match(r".*(ESP\d+).*", stdout_text_input)
        flash_size_match = re.match(r".*(\d+MB).*", stdout_text_input)

        if read_match:
            read_in_progress = re.match(r"^\d+ \((\d+) %\)", read_match.group(1))
            if read_in_progress:
                flashing_in_progress = read_in_progress.group(1)
                self.progress_bar["value"] = int(flashing_in_progress)

            last_insert = self.text_area.tag_ranges("tag_read_procent")
            if len(last_insert) > 1:
                self.text_area.delete(last_insert[0], last_insert[1])

            self.text_area.insert(
                tk.END, f"{read_match.group(1)}\n", "tag_read_procent")

            self.text_area.see(tk.END)
        elif write_match:
            flashing_in_progress = write_match.group(2)
            text = write_match.group(1)

            self.progress_bar["value"] = int(flashing_in_progress)

            last_insert = self.text_area.tag_ranges("tag_write_procent")
            if len(last_insert) > 1:
                self.text_area.delete(last_insert[0], last_insert[1])
                self.text_area.delete("end-1c", tk.END)

            self.text_area.insert(tk.END, text, "tag_write_procent")
            self.text_area.see(tk.END)
        elif esp_type_match:
            # input contains only part of string e.g. ' ESP32' or 'ESP32-D0WDQ6 (revision 1)'
            self.esp_type = esp_type_match.group(1)
            self.normal_output(stdout_text_input)
        elif flash_size_match:
            self.esp_flash_size = flash_size_match.group(1)
            self.normal_output(stdout_text_input)
        else:
            self.normal_output(stdout_text_input)
