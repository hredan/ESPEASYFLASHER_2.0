'''
  SerialMonitor.py can start and stop a serial connection to an ESP microcontroller.
  It is used by ESPEasyFlasher.py to get the output from Serial interface of ESP microcontroller.
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

  Some of the code is bases on wxTerminal example (SPDX-License-Identifier:    BSD-3-Clause):
  https://github.com/pyserial/pyserial/blob/master/examples/wxTerminal.py
'''

import serial
import threading
import time

import tkinter as tk

NEWLINE_CR = 0
NEWLINE_LF = 1
NEWLINE_CRLF = 2

class TerminalSetup:
    """
    Placeholder for various terminal settings. Used to pass the
    options to the TerminalSettingsDialog.
    """
    def __init__(self):
        self.echo = False
        self.unprintable = False
        self.newline = NEWLINE_CRLF

class SerialMonitor:
    def __init__(self, text_area):
        self.serial = serial.Serial()
        self.settings = TerminalSetup()
        self.serial.timeout = 0.5
        self.serial.baudrate = 115200
        self.serial.stopbits = 1
        self.serial.bytesize = 8


        self.thread = None
        self.alive = threading.Event()

        self.text_area = text_area

    def espReset(self):
        if (self.serial.rts and self.serial.dtr):
            self.serial.rts = False
            self.serial.dtr = False
            time.sleep(0.1)
            self.serial.rts = True
            self.serial.dtr = True
        else:
            self.serial.rts = True
            self.serial.dtr = True

    def StartThread(self, comport):
        """Start the receiver thread"""
        try:
            self.serial.port = comport
            self.serial.open()
           
        except serial.SerialException as e:
            self.text_area.insert(tk.END, f"Error open serial connection: {e}")
        else:
            self.text_area.insert(tk.END, "### open serial connection ###\n")
            
            self.thread = threading.Thread(target=self.ComPortThread)
            self.thread.setDaemon(1)
            self.alive.set()
            self.thread.start()
            self.serial.rts = True
            self.serial.dtr = True
    
    def StopThread(self):
        """Stop the receiver thread, wait until it's finished."""
        if self.thread is not None:
            self.alive.clear()          # clear alive event for thread
            self.thread.join()          # wait until thread has finished
            self.thread = None
            self.serial.close()
            self.text_area.insert(tk.END, "### close serial connection ###\n")

    def ComPortThread(self):
        """\
        Thread that handles the incoming traffic. Does the basic input
        transformation (newlines) and generates an SerialRxEvent
        """
        while self.alive.isSet():
            b = self.serial.read(self.serial.in_waiting or 1)
            if b:
                # newline transformation
                if self.settings.newline == NEWLINE_CR:
                    b = b.replace(b'\r', b'\n')
                elif self.settings.newline == NEWLINE_LF:
                    pass
                elif self.settings.newline == NEWLINE_CRLF:
                    b = b.replace(b'\r\n', b'\n')
                self.text_area.insert(tk.END, b)
                self.text_area.see(tk.END)