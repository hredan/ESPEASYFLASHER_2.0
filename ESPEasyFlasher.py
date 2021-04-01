
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
import os
import threading
import re
import json
import glob

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
        mObjRead = re.match("^(\d+ \(\d+ %\)).*", input)
        mObjWrite = re.match("^(Writing .+\((\d+) %\)).*", input)
        if(mObjRead):
            numG1 = len(mObjRead.group(1))
            reProgress = re.match("^\d+ \((\d+) %\)", mObjRead.group(1))
            if(reProgress):
                flashProgress = reProgress.group(1)
                self.progressBar["value"] = int(flashProgress)

            last_insert = self.text_area.tag_ranges("tag_read_procent")
            if (len(last_insert) > 1):
                self.text_area.delete(last_insert[0], last_insert[1])

            self.text_area.insert(tk.END, f"{mObjRead.group(1)}\n", "tag_read_procent")

            # just for testing
            # self.text_area.insert(tk.END, f"{numG1}:{mObj.group(1)} {numG2}\n")
            self.text_area.see(tk.END)
        elif(mObjWrite):
            flashProgress = mObjWrite.group(2)
            text = mObjWrite.group(1)
            
            self.progressBar["value"] = int(flashProgress)
            
            last_insert = self.text_area.tag_ranges("tag_write_procent")
            if (len(last_insert) > 1):
                self.text_area.delete(last_insert[0], last_insert[1])
                self.text_area.delete("end-1c", tk.END)

            self.text_area.insert(tk.END, text, "tag_write_procent")
            self.text_area.see(tk.END)
        else:
            self.text_area.insert(tk.END, input)
            self.text_area.see(tk.END)


    def flush(self):
        pass
    
    def isatty(self):
        return False

class App:
    def logoFileExists(self):
        returnValue = False
        filename = "./LogoEasyFlash.png"
        if (os.path.exists(filename)):
            self.logoFilename = filename
            returnValue = True
        elif (self.checkMAIPASS()):
            self.logoFilename = os.path.join(self.basePath, filename)
            returnValue = True
        else:
            returnValue = False
            self.strIo.write(f"Warning: Could not find '{filename}', using layout without logo!\n")

        return returnValue

    def gridWithoutLogo(self):
        self.comGroup.grid(column=0, row=rowPosFrame, columnspan = 3, sticky="EW", padx=5, pady=5)

    def __init__(self, master):
        self.developerMode = True
        self.withLogo = True
        self.strIo = StringIO()
        
        self.strIo.write(f"os: {sys.platform}\n")
        if ((sys.platform != "win32") and (self.checkMAIPASS())):
            path = os.path.sep.join(sys.argv[0].split(os.path.sep))
            dirname = os.path.dirname(path)
            os.chdir(dirname)
            self.strIo.write(f"{dirname}\n")
        
        self.strIo.write(f"CWD: {os.getcwd()}\n")
        
        # read config from json file
        self.readConfig()

        master.title("ESPEasyFlasher2.0")
        master.resizable(0, 0)        
        
        frame = ttk.Frame(master)
        frame.pack()
        
        rowPosFrame = 0
        self.comGroup = tk.LabelFrame(frame, text='Serial Com Port')
        

        if (self.withLogo):
            if (self.logoFileExists()):
                self.comGroup.grid(column=0, row=rowPosFrame, sticky="EW", padx=5, pady=5)
                self.logo = tk.PhotoImage(file=self.logoFilename)
                self.labelLogo = tk.Label(frame, image=self.logo)
                self.labelLogo.grid(column=1, row=rowPosFrame, columnspan = 2, sticky="EW")
            else:
                self.gridWithoutLogo()
        else:
            self.gridWithoutLogo()

        # Com Port
        rowPosCom = 0
        self.labelComPort = tk.Label(self.comGroup, text="Com Port: ")
        self.labelComPort.grid(column=0, row=rowPosCom, sticky="W")

        self.comboComPort = ttk.Combobox(self.comGroup)
        self.comboComPort.grid(column=1, row=rowPosCom, sticky="WE", padx=3, pady=3)

        rowPosCom += 1
        self.comRefreshBtn = tk.Button(self.comGroup, text="Scan", command=self.comScan)
        self.comRefreshBtn.grid(column=0, row=rowPosCom, columnspan = 2, sticky="WE", padx=3, pady=3)
        
        tk.Grid.columnconfigure(self.comGroup, 0, weight=1)
        tk.Grid.columnconfigure(self.comGroup, 1, weight=2)

        # write Group
        rowPosFrame += 1
        self.writeGroup = tk.LabelFrame(frame, text='WriteFlash')
        self.writeGroup.grid(column=0, row=rowPosFrame, columnspan = 3, sticky="EW", padx=5, pady=5)

        rowPosWrite = 0
        self.labelWriteBin = tk.Label(self.writeGroup, text="bin file: ")
        self.labelWriteBin.grid(column=0, row=rowPosWrite, sticky="W")

       
        self.comboWriteBin = ttk.Combobox(self.writeGroup)
        self.setFileListComboWrite()
        self.comboWriteBin.grid(column=1, row=rowPosWrite, sticky="EW", padx=3, pady=3)
        
        rowPosWrite += 1
        self.button = tk.Button(self.writeGroup, text="WriteFlash", command=self.writeFlash)
        self.button.grid(column=0, row=rowPosWrite, columnspan = 2, sticky="EW", padx=3, pady=3)
   
        tk.Grid.columnconfigure(self.writeGroup, 0, weight=1)
        tk.Grid.columnconfigure(self.writeGroup, 1, weight=2)

        # read Group
        if (self.developerMode):
            rowPosFrame += 1
            self.readGroup = tk.LabelFrame(frame, text='ReadFlash')
            self.readGroup.grid(column=0, row=rowPosFrame, columnspan = 3, sticky="EW", padx=5, pady=5)

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
            self.eraseGroup.grid(column=0, row=rowPosFrame, columnspan = 3, sticky="EW", padx=5, pady=5)

            rowPosErase = 0
            self.readBtn = tk.Button(self.eraseGroup, text="EraseFlash", command=self.eraseFlash)
            self.readBtn.grid(column=0, row=rowPosRead, sticky="EW", padx=3, pady=3)

            tk.Grid.columnconfigure(self.eraseGroup, 0, weight=1)

        # Textbox Logging
        rowPosFrame += 1
        self.text_box = tk.Text(frame, wrap='word', height = 11, width=80)
        self.text_box.grid(column=0, row=rowPosFrame, columnspan = 2, sticky="EW", padx=5, pady=5)
        

        scrollb = ttk.Scrollbar(frame, command=self.text_box.yview)
        scrollb.grid(row=rowPosFrame, column=2, sticky='nsew')
        self.text_box['yscrollcommand'] = scrollb.set

        

        # Progressbar
        rowPosFrame += 1
        self.progress = ttk.Progressbar(frame, orient="horizontal",
                                        length=200, mode="determinate")
        self.progress.grid(column=0, row=rowPosFrame, columnspan = 2, sticky="EW", padx=5, pady=5)

        sys.stdout = StdoutRedirector(self.text_box, self.progress)

        # write config string
        self.text_box.insert(tk.END, self.strIo.getvalue())
        
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

    def readEEF(self, filename):
        self.strIo.write("### read eef file ###\n")
        returnValue = ""
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                returnValue = data['command']

        except EnvironmentError as err:
            self.strIo.writelines(f"Error could not read eef file {filename}: {err}\n")
        return returnValue

    def writeFlash(self):
        self.progress["value"] = 0
        self.progress["maximum"] = 100
        print("### Write Flash")
        comPort = self.comboComPort.get()
        filename = self.comboWriteBin.get()
        if (comPort == ""):
            print("Error: select a Serial Com Port before you can start read flash!")
        elif (filename == ""):
            print("Error: before you can write to flash, select a firmware.bin file")
        else:
            file_name, file_extension = os.path.splitext(filename)
            if (file_extension == ".eef"):
                command = self.readEEF(filename)
                x = threading.Thread(target=EsptoolCom.esptoolWriteEEF, args=(comPort, command,))
            else:
                x = threading.Thread(target=EsptoolCom.esptoolWriteFlash, args=(comPort, filename,))
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
            filename = filename + ".bin"
            x = threading.Thread(target=EsptoolCom.esptoolReadFlash, args=(comPort, filename,))
            x.start()

    def getFileListBin(self):
        fileList = glob.glob("*.eef")
        if (len(fileList) == 0):
            fileList = glob.glob("*.bin")
        return fileList

    def setFileListComboWrite(self):
        fileList = self.getFileListBin()
        self.comboWriteBin["values"] = fileList
        if(len(fileList) > 0):
            self.comboWriteBin.current(0)

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
            defaultCom = comlist[0].device

        isFundUsbSerial = False
        for com in comlist:
            # print(com.name)
            print("*" + com.description)
            clist.append(com.device)
            if(com.description.lower().find("usb") != -1 ):
                defaultCom = com.device
                print("Found: "+defaultCom)
                isFundUsbSerial = True

        if (isFundUsbSerial != True):
            print("Warning: could not find a usb-serial device, connect your device and scan again!")

        return {"comlist": clist, "defaultCom": defaultCom}

    def readConfig(self):
        self.strIo.write("### Read Config ###\n")
        try:
            with open('ESPEasyFlasherConfig.json') as json_file:
                data = json.load(json_file)
                
                self.withLogo = data['logo']
                self.strIo.writelines(f"enable logo: {data['logo']}\n")

                self.developerMode = data['devMode']
                self.strIo.writelines(f"dev mode is: {data['devMode']}\n")
                
                EsptoolCom.baudRate = data['baudRate']
                self.strIo.write(f"set baud rate to: {data['baudRate']}\n")
                
                EsptoolCom.readStart = data['readStart']
                self.strIo.write(f"set read start to: {data['readStart']}\n")
                
                EsptoolCom.readSize = data['readSize']
                self.strIo.write(f"set read size to: {data['readSize']}\n")
                
                EsptoolCom.writeStart = data['writeStart']
                self.strIo.write(f"set write start to: {data['writeStart']}\n")

        except EnvironmentError as err:
            self.strIo.writelines(f"Error could not read config, default values will be used: {err}\n")

    def checkMAIPASS(self):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        returnValue = False
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            self.basePath = sys._MEIPASS
            returnValue = True
        except Exception:
            self.basePath = os.path.abspath(".")
            returnValue = False

        return returnValue

if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()