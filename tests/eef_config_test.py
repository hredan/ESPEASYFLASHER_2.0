"""
  eef_config_test contains unittest for eef_config.py
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

import sys
import os
import unittest
from unittest.mock import Mock
from io import StringIO

import tests
from eef_modules.eef_helper.eef_config import EEFConfig


class EEFConfigTests(unittest.TestCase):
    """ Test class for EEFConfig"""
    def test_default_values(self):
        """ tests the default values of EEFConfig """
        esp = Mock()
        str_io = StringIO()

        logo_path = tests.test_dir + "/test_data/fake_logo.png"
        eef_config = EEFConfig("na_config.json", logo_path, str_io, esp)

        # check default values
        self.assertEqual(eef_config.with_logo(), True)
        self.assertEqual(eef_config.with_developer_mode(), True)
        self.assertEqual(eef_config.with_serial_monitor(), True)
        self.assertEqual(eef_config.with_esp_info(), True)

        self.assertEqual(eef_config.get_logo_file_path(), logo_path)
        self.assertEqual(eef_config.is_pyinstaller(), False)
        self.assertEqual(eef_config.get_base_path(), os.path.abspath(".."))

    def test_config_read(self):
        """ tests the read out of config json file """
        esp = Mock()
        str_io = StringIO()

        logo_path = tests.test_dir + "/test_data/fake_logo.png"
        config_path = tests.test_dir + "/test_data/ESPEasyFlasherConfig_test.json"
        eef_config = EEFConfig(config_path, logo_path, str_io, esp)

        self.assertEqual(eef_config.with_logo(), False)
        self.assertEqual(eef_config.with_developer_mode(), False)
        self.assertEqual(eef_config.with_serial_monitor(), False)
        self.assertEqual(eef_config.with_esp_info(), False)

        self.assertEqual(esp.baud_rate, '460801')
        self.assertEqual(esp.read_start, '0x00001')
        self.assertEqual(esp.read_size, '0x100000')
        self.assertEqual(esp.write_start, '0x00002')

    def test_meipass(self):
        """ tests meipass created by PyInstaller"""

        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # pylint: disable=protected-access
        sys._MEIPASS = "test"

        esp = Mock()
        str_io = StringIO()

        logo_path = tests.test_dir + "/test_data/fake_logo.png"
        config_path = tests.test_dir + "/test_data/ESPEasyFlasherConfig_test.json"
        eef_config = EEFConfig(config_path, logo_path, str_io, esp)
        self.assertEqual(eef_config.is_pyinstaller(), True)
        self.assertEqual(eef_config.get_base_path(), "test")

        # remove attribute _MEIPASS
        delattr(sys, "_MEIPASS")

    def test_missing_logo(self):
        """ tests missing logo """
        esp = Mock()
        str_io = StringIO()

        config_path = "no_config.json"
        logo_path = "no_logo.png"

        # no_config to get default values logo true, but logo file is not available then logo false
        eef_config = EEFConfig(config_path, logo_path, str_io, esp)

        self.assertEqual(eef_config.with_logo(), False)
        self.assertEqual(eef_config.get_logo_file_path(), None)

    def test_missing_logo_meipass(self):
        """ tests missing logo if PyInstaller is used"""
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        # pylint: disable=protected-access
        sys._MEIPASS = "test"
        esp = Mock()
        str_io = StringIO()

        config_path = "no_config.json"
        logo_path = "no_logo.png"

        # no_config to get default values logo true, but logo file is not available then logo false
        eef_config = EEFConfig(config_path, logo_path, str_io, esp)

        self.assertEqual(eef_config.with_logo(), False)
        self.assertEqual(eef_config.get_logo_file_path(), None)

        # remove attribute _MEIPASS
        delattr(sys, "_MEIPASS")
