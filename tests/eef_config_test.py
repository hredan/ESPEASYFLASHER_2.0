import sys
import os
import unittest
from unittest.mock import Mock
from io import StringIO

import tests
from eef_modules.eef_helper.eef_config import EEFConfig


class EEFConfigTests(unittest.TestCase):

    def test_default_values(self):
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
        esp = Mock()
        str_io = StringIO()

        config_path = "no_config.json"
        logo_path = "no_logo.png"

        # no_config to get default values logo true, but logo file is not available then logo false
        eef_config = EEFConfig(config_path, logo_path, str_io, esp)

        self.assertEqual(eef_config.with_logo(), False)
        self.assertEqual(eef_config.get_logo_file_path(), None)

    def test_missing_logo_meipass(self):
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
