'''
  ESPEasyFlasher.py is a Simple GUI for esptool.py by espressif
  (https://github.com/espressif/esptool)
  
  It is also written in Python and is using Tkinter as GUI framework.

  Targets:
    * Using should be simple, also for people without experience of command line tools
    * It can be easily configured by experienced people and user of the esptool.py
    * It can be used in two modes (Developer/User)
    * It is platform independent same as esptool.py 
  
  Copyright (C) 2021  André Herrmann
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

import sys
import threading
import re
import json

import tkinter as tk
from tkinter import ttk

from serial.tools.list_ports import comports

import EsptoolCom

from io import StringIO

# With Flag developerMode you can expand the use cases in the GUI with read and erase flash


class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self,text_area, progressBar):
        self.text_area = text_area
        self.progressBar = progressBar

class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    
    def write(self, input):
        mObj = re.match("^(\d+ \(\d+ %\)).*", input)
        if(mObj):
            numG1 = len(mObj.group(1))
            reProgress = re.match("^\d+ \((\d+) %\)", mObj.group(1))
            if(reProgress):
                flashProgress = reProgress.group(1)
                self.progressBar["value"] = int(flashProgress)

            last_insert = self.text_area.tag_ranges("tag_procent")
            if (len(last_insert) > 1):
                self.text_area.delete(last_insert[0], last_insert[1])

            self.text_area.insert(tk.END, f"{mObj.group(1)}\n", "tag_procent")

            # just for testing
            # self.text_area.insert(tk.END, f"{numG1}:{mObj.group(1)} {numG2}\n")
            self.text_area.see(tk.END)
        else:
            self.text_area.insert(tk.END, input)
            self.text_area.see(tk.END)


    def flush(self):
        pass
    
    def isatty(self):
        return False

class App:
    def __init__(self, master):
        self.developerMode = True
        
        # read config from json file
        configStr = self.readConfig()

        master.title("ESPEasyFlasher2.0")
        master.resizable(0, 0)        
        
        frame = ttk.Frame(master)
        frame.pack()
        
        rowPosFrame = 0
        self.comGroup = tk.LabelFrame(frame, text='Serial Com Port')
        self.comGroup.grid(column=0, row=rowPosFrame, sticky="EW", padx=5, pady=5)

        # Com Port
        rowPosCom = 0
        self.labelComPort = tk.Label(self.comGroup, text="Com Port: ")
        self.labelComPort.grid(column=0, row=rowPosCom, sticky="W")

        self.comboComPort = ttk.Combobox(self.comGroup)
        self.comboComPort.grid(column=1, row=rowPosCom, sticky="EW", padx=3, pady=3)

        rowPosCom += 1
        self.comRefreshBtn = tk.Button(self.comGroup, text="Scan", command=self.comScan)
        self.comRefreshBtn.grid(column=0, row=rowPosCom, columnspan = 2, sticky="EW", padx=3, pady=3)
        
        tk.Grid.columnconfigure(self.comGroup, 0, weight=1)
        tk.Grid.columnconfigure(self.comGroup, 1, weight=2)

        # write Group
        rowPosFrame += 1
        self.writeGroup = tk.LabelFrame(frame, text='WriteFlash')
        self.writeGroup.grid(column=0, row=rowPosFrame, sticky="EW", padx=5, pady=5)

        rowPosWrite = 0
        self.labelWriteBin = tk.Label(self.writeGroup, text="bin file: ")
        self.labelWriteBin.grid(column=0, row=rowPosWrite, sticky="W")

        self.comboWriteBin = ttk.Combobox(self.writeGroup)
        self.comboWriteBin.grid(column=1, row=rowPosWrite, sticky="EW", padx=3, pady=3)
        
        rowPosWrite += 1
        self.button = tk.Button(self.writeGroup, 
                            text="WriteFlash")
        self.button.grid(column=0, row=rowPosWrite, columnspan = 2, sticky="EW", padx=3, pady=3)
   
        tk.Grid.columnconfigure(self.writeGroup, 0, weight=1)
        tk.Grid.columnconfigure(self.writeGroup, 1, weight=2)

        # read Group
        if (self.developerMode):
            rowPosFrame += 1
            self.readGroup = tk.LabelFrame(frame, text='ReadFlash')
            self.readGroup.grid(column=0, row=rowPosFrame, sticky="EW", padx=5, pady=5)

            rowPosRead = 0
            self.labelReadBin = tk.Label(self.readGroup, text="Flash write to: ")
            self.labelReadBin.grid(column=0, row=rowPosRead, sticky="W")

            defaultText = tk.StringVar(self.readGroup, value="filename_read_flash")
            self.entryFileName = tk.Entry(self.readGroup, width=20, textvariable=defaultText)
            self.entryFileName.grid(column=1, row=rowPosRead, sticky="EW")

            self.fileExtension = tk.Label(self.readGroup, text=".bin")
            self.fileExtension.grid(column=2, row=rowPosRead, sticky="W")

            rowPosRead += 1
            self.readBtn = tk.Button(self.readGroup, text="ReadFlash", command=self.readFlash)
            self.readBtn.grid(column=0, row=rowPosRead, columnspan = 3, sticky="EW", padx=3, pady=3)

            tk.Grid.columnconfigure(self.readGroup, 0, weight=1)
            tk.Grid.columnconfigure(self.readGroup, 1, weight=2)
            tk.Grid.columnconfigure(self.readGroup, 2, weight=1)

            rowPosFrame += 1
            self.eraseGroup = tk.LabelFrame(frame, text='EraseFlash')
            self.eraseGroup.grid(column=0, row=rowPosFrame, sticky="EW", padx=5, pady=5)

            rowPosErase = 0
            self.readBtn = tk.Button(self.eraseGroup, text="EraseFlash", command=self.eraseFlash)
            self.readBtn.grid(column=0, row=rowPosRead, sticky="EW", padx=3, pady=3)

            tk.Grid.columnconfigure(self.eraseGroup, 0, weight=1)

        # Textbox Logging
        rowPosFrame += 1
        self.text_box = tk.Text(frame, wrap='word', height = 11, width=80)
        self.text_box.grid(column=0, row=rowPosFrame, sticky="EW", padx=5, pady=5)
        

        scrollb = ttk.Scrollbar(frame, command=self.text_box.yview)
        scrollb.grid(row=rowPosFrame, column=1, sticky='nsew')
        self.text_box['yscrollcommand'] = scrollb.set

        

        # Progressbar
        rowPosFrame += 1
        self.progress = ttk.Progressbar(frame, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress.grid(column=0, row=rowPosFrame, columnspan = 2, sticky="EW", padx=5, pady=5)

        sys.stdout = StdoutRedirector(self.text_box, self.progress)

        # write config string
        self.text_box.insert(tk.END, configStr)
        
        # scan com ports
        self.comScan()

    def eraseFlash(self):
        print("### Erase Flash ###")
        comPort = self.comboComPort.get()
        if (comPort == ""):
            print("Error: select a Serial Com Port before you can start read flash!")
        else:
            x = threading.Thread(target=EsptoolCom.esptoolEraseFlash, args=(comPort,))
            x.start()

    def readFlash(self):
        self.progress["value"] = 0
        self.progress["maximum"] = 100

        print("### Read Flash ###")
        comPort = self.comboComPort.get()
        filename = self.entryFileName.get()
        if (comPort == ""):
            print("Error: select a Serial Com Port before you can start read flash!")
        elif (filename == ""):
            print("Error: before you can read flash, define a filename")
        else:
            x = threading.Thread(target=EsptoolCom.esptoolReadFlash, args=(comPort, filename,))
            x.start()
            

    def comScan(self):
        comInfo = self.getComInfo()
        if (len(comInfo["comlist"]) > 0):
            self.comboComPort["values"] = comInfo["comlist"]            
            
            if(comInfo["defaultCom"] != ""):
                self.comboComPort.current(comInfo["comlist"].index(comInfo["defaultCom"]))
            else:
                self.comboComPort.current(0)


    def getComInfo(self):
        print("### Com Port Scan ###")
        clist = []
        defaultCom = ""
        
        comlist = comports()
        print("Number of Com Ports: " + str(len(comlist)))
        if (len(comlist) > 0):
            defaultCom = comlist[0].name

        isFundUsbSerial = False
        for com in comlist:
            # print(com.name)
            print("*" + com.description)
            clist.append(com.name)
            if(com.description.lower().find("usb-serial") != -1 ):
                defaultCom = com.name
                print("Found: "+defaultCom)
                isFundUsbSerial = True

        if (isFundUsbSerial != True):
            print("Warning: could not find a usb-serial device, connect your device and scan again!")

        return {"comlist": clist, "defaultCom": defaultCom}

    def readConfig(self):
        strIo = StringIO()
        strIo.write("### Read Config ###\n")
        try:
            with open('ESPEasyFlasherConfig.json') as json_file:
                data = json.load(json_file)
                
                self.developerMode = data['devMode']
                strIo.writelines(f"dev mode is: {data['devMode']}\n")
                
                EsptoolCom.baudRate = data['baudRate']
                strIo.write(f"set baud rate to: {data['baudRate']}\n")
                
                EsptoolCom.readStart = data['readStart']
                strIo.write(f"set read start to: {data['readStart']}\n")
                
                EsptoolCom.readSize = data['readSize']
                strIo.write(f"set read size to: {data['readSize']}\n")
                
                EsptoolCom.writeStart = data['writeStart']
                strIo.write(f"set write start to: {data['writeStart']}\n")

        except EnvironmentError as err:
            strIo.writelines(f"Error could not read config, default values will be used: {err}\n")
        
        return strIo.getvalue()

if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()