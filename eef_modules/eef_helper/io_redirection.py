"""
  io_redirection.py is used by ESPEasyFlasher.py to redirect and filter
  the stdout and stderr to the TK text_area.
  https://github.com/hredan/ESPEASYFLASHER_2.0

  Copyright (C) 2026  André Herrmann (hredan)
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
import re


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


class IORedirection:
    """A general class for redirecting I/O to this Text widget."""
    def __init__(self, text_area, progress_bar):
        self.text_area = text_area
        self.progress_bar = progress_bar
        self.text_area.tag_config("error", foreground="red")

    def flush(self):
        """dummy flush needed for IO"""

    @classmethod
    def isatty(cls):
        """dummy isatty needed for IO"""
        return False


class StderrRedirection(IORedirection):
    """A class for redirecting stderr to this Text widget."""
    def write(self, stderr_text_input):
        """
        write method, filtered the Stderr and adept the text before insert to the text_area

        Parameters:
        stderr_text_input (str): raw stderr input
        """
        self.text_area.insert(tk.END, stderr_text_input, "error")
        self.text_area.see(tk.END)


class StdoutRedirection(IORedirection):
    """A class for redirecting stdout to this Text widget."""

    def __init__(self, text_area, progress_bar):
        super().__init__(text_area, progress_bar)
        self.esp_type = None
        self.esp_flash_size = None
        self.stdout_progress_buffer = ""

    def normal_output(self, text_area_output):
        """
        standard method to insert text to text_area

        Parameters:
        input (str): text input
        """
        self.text_area.insert(tk.END, text_area_output)
        self.text_area.see(tk.END)

    @staticmethod
    def _clean_stdout_text(stdout_text_input):
        clean_stdout_text = ANSI_ESCAPE_RE.sub("", stdout_text_input)
        clean_stdout_text = clean_stdout_text.replace("\r", "")
        clean_stdout_text = re.sub(r"^\[K", "", clean_stdout_text)
        return clean_stdout_text

    def _update_read_progress(self, read_match):
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

    def _update_write_progress_line(self, write_match_new):
        flashing_in_progress = int(float(write_match_new.group(2)))
        text = write_match_new.group(1)

        if not text.endswith("\n"):
            text += "\n"

        self.progress_bar["value"] = flashing_in_progress

        last_insert = self.text_area.tag_ranges("tag_write_procent")
        if len(last_insert) > 1:
            self.text_area.delete(last_insert[0], last_insert[1])

        if self.text_area.index("end-1c") != "1.0":
            last_char = self.text_area.get("end-2c", "end-1c")
            if last_char != "\n":
                self.text_area.insert(tk.END, "\n")

        self.text_area.insert(tk.END, text, "tag_write_procent")
        self.text_area.see(tk.END)

    def _extract_write_progress_from_buffer(self, clean_stdout_text):
        write_progress = None

        # New format: Writing at ... 16.1% 32768/203648 bytes...
        write_progress_pattern = (
            r"Writing .*?(\d+(?:\.\d+)?)%\s+\d+/\d+\s+bytes"
        )
        for new_match in re.finditer(
            write_progress_pattern,
            self.stdout_progress_buffer):
            write_progress = int(float(new_match.group(1)))

        # Some esptool runs only print the final summary line.
        if (
            write_progress is None
            and re.search(r"Wrote \d+ bytes .* in .* seconds", clean_stdout_text)
        ):
            write_progress = 100

        return write_progress

    def _handle_device_info_output(self, clean_stdout_text):
        esp_type_match = re.match(r".*(ESP\d+).*", clean_stdout_text)
        flash_size_match = re.match(r".*(\d+MB).*", clean_stdout_text)

        if esp_type_match:
            # input contains only part of string e.g. ' ESP32' or 'ESP32-D0WDQ6 (revision 1)'
            self.esp_type = esp_type_match.group(1)
            self.normal_output(clean_stdout_text)
            return

        if flash_size_match:
            self.esp_flash_size = flash_size_match.group(1)
            self.normal_output(clean_stdout_text)
            return

        self.normal_output(clean_stdout_text)

    def write(self, stdout_text_input):
        """
        write method, filtered the Stdout and adept the text before insert to the text_area

        Parameters:
        stdout_text_input (str): raw stdout input
        """
        clean_stdout_text = self._clean_stdout_text(stdout_text_input)

        # Keep a rolling buffer so progress can still be detected when esptool output
        # arrives in partial chunks.
        self.stdout_progress_buffer += clean_stdout_text
        self.stdout_progress_buffer = self.stdout_progress_buffer[-2048:]

        read_match = re.search(r"(\d+ \(\d+ %\))", clean_stdout_text)
        write_match_new = re.search(r"(Writing .*?(\d+(?:\.\d+)?)%).*", clean_stdout_text)

        if read_match:
            self._update_read_progress(read_match)
            return

        if write_match_new:
            self._update_write_progress_line(write_match_new)
            return

        write_progress = self._extract_write_progress_from_buffer(clean_stdout_text)
        if write_progress is not None:
            self.progress_bar["value"] = write_progress

        self._handle_device_info_output(clean_stdout_text)
