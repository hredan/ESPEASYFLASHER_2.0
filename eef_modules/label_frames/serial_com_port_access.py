"""
  serial_com_port_access.py is used by ESPEasyFlasher.py.
  It is a helper class to get a list of available com ports in the OS.
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

from serial.tools.list_ports import comports


# for the helper class only one class method is available
# pylint: disable=too-few-public-methods
class SerialComPortAccess:
    """ Helper class to get a list of com ports"""
    @classmethod
    def get_com_info(cls):
        """ get comports by serial.tools.list_ports
            and returns a list of usb com ports and the first usb com port as default
        """
        print("### Com Port Scan ###")
        usb_com_list = []
        default_com = ""

        com_ports = comports()
        print("Number of Com Ports: " + str(len(com_ports)))
        if len(com_ports) > 0:
            default_com = com_ports[0].device

        is_found_usb_serial_com_port = False
        for com in com_ports:
            # print(com.name)
            print("*" + com.description)
            usb_com_list.append(com.device)
            if com.description.lower().find("usb") != -1:
                default_com = com.device
                print("Found: " + default_com)
                is_found_usb_serial_com_port = True

        if not is_found_usb_serial_com_port:
            print(
                "Warning: could not find a usb-serial device, connect your device and scan again!")

        return {"comlist": usb_com_list, "defaultCom": default_com}
