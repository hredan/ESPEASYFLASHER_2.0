'''
  EsptoolCom.py is a simple python interface to esptool.py (https://github.com/espressif/esptool).
  It is used by ESPEasyFlasher.py to write, read, and erase flash of esp microcontroller.
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
import esptool

# Config variables can be changed by EspEasyFlasherConfig.json
baudRate = '460800'

readStart = '0'
readSize = '0x400000'

writeStart = '0x00000'

def esptoolReadFlash(comPort, filename):
    #for testing a short byte array
    command = ['--port', comPort, '--baud', baudRate, 'read_flash', readStart, readSize, filename]
    #command = ['--port', comPort, '--baud', '460800', 'read_flash', '0', '0x400000', 'flash_contents.bin']      
    startEsptool(command)

def esptoolWriteFlash(comPort, filename):
    command = ['--port', comPort, '--baud', baudRate, 'write_flash', writeStart, filename]
    startEsptool(command)

def esptoolEraseFlash(comPort):
    command = ['--port', comPort, 'erase_flash']
    startEsptool(command)

def startEsptool(command):
    print('Using command %s' % ' '.join(command))
    esptool.main(command)
    