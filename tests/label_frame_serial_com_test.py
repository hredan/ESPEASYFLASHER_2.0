"""
  label_frame_serial_com_test contains unittest for serial_com.py
  It is part of ESPEasyFlasher tests.
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

import unittest
from unittest.mock import call, Mock

import tests
from eef_modules.label_frames.serial_com import SerialComLabelFrame


class SerialComTest(unittest.TestCase):
    """ unit tests for label frame serial_com"""
    def setUp(self):
        """ setup creates root and frame for every test"""
        self.root = tk.Tk()
        self.frame = ttk.Frame(self.root)
        self.frame.pack()

    def tearDown(self):
        """ tear down destroy root for every test"""
        self.root.destroy()

    def test_serial_com(self):
        """ test create SerialComLabelFrame instance"""
        eef_config = Mock()
        serial_com = SerialComLabelFrame(self.frame, eef_config)
        self.assertIsNotNone(serial_com)

    def test_serial_com_set_pos(self):
        """ test  serial_com.set_positioning without logo and esp_info """

        expected_calls_eef_config = [call.with_logo(), call.with_esp_info()]
        self.set_pos(False, False, expected_calls_eef_config, [])

    def test_serial_com_set_pos_with_logo(self):
        """ test  serial_com.set_positioning with logo and esp_info """
        expected_calls_eef_config = [call.with_logo(), call.get_logo_file_path(),
                                     call.with_esp_info()]

        self.set_pos(True, True, expected_calls_eef_config, [])

    def set_pos(self, with_logo, with_esp_info, expected_calls_eef_config, expected_calls_esp_func):
        """ sub method for serial_com.set_positioning tests """
        esp_func_calls = Mock()
        eef_config = Mock()

        eef_config.with_logo.return_value = with_logo
        eef_config.with_esp_info.return_value = with_esp_info

        if with_logo:
            eef_config.get_logo_file_path.return_value = tests.test_dir + "/../LogoEasyFlash.png"

        serial_com = SerialComLabelFrame(self.frame, eef_config)
        serial_com.set_positioning(0, esp_func_calls)

        self.assertEqual(eef_config.mock_calls, expected_calls_eef_config)
        self.assertEqual(esp_func_calls.mock_calls, expected_calls_esp_func)
