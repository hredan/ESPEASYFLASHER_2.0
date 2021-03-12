# ESPEasyFlasher_2.0 is a GUI written in python for the command line tool esptool

## Why I have implemented ESPEasyFlasher_2.0
I was searching for a simple tool to share firmware binaries for the DIY-Project SleepUINO. The SleepUINO is a alarm clock with a web interface based on a ESP8266. Currently the SleepUINO code is not public, but you can find some information in German on www.sleepuino.info

What I have found was the command line tool [esptool.py](https://github.com/espressif/esptool) from espressif. It can be used to flash all ESP micro controller, it is a good base and the community is working on it. It is alive! And I have found some different GUIs. Some GUIs try to contain the whole functionality of the esptool and are very complex. I want a simple tool to share my firmware without any frills, like the [ESPEASYFLASHER](https://github.com/BattloXX/ESPEasyFlasher) from BattloXX. But this GUI is only usable on Windows. I want a GUI that is platform independently. So I have got ideas but I have not found a satisfactory solution.

## Build my own GUI based on esptool and tkinter called ESPEasyFlasher_2.0
I liked the simple usability of ESPEasyFlasher from BattloXX but I could not understand why it is implemented in C#. The esptool is not only a command line tool, it has also a python interface. Python itself is platform independently and contains tkinter, [a Python binding to the Tk GUI toolkit](https://en.wikipedia.org/wiki/Tkinter), as standard library. And the icing on the cake, with [pyinstaller](https://www.pyinstaller.org/) it is possible to generate executables for different os platforms. So why not implementing all things in Python and bring the idea of ESPEasyFlasher to the next level 2.0.

# Functionality of ESPEasyFlasher_2.0
## Configuration by Json file
With the json file ESPEasyFlasherConfig.json you can change the layout and behavior of esptool. You can switch between a developer layout, there you can readout the flash in a file. And you can erase the flash. It is also very simple and you can change some behavior of esptool parameter, this is for people who have experience with the esptool.py self.

## Developer Layout, to create firmware files


## User Layout, to share a ESP firmware in a simple way
This is the simple layout to share your firmware with people who are not able to compile your Arduino source code but they want build a DIY-Project based on ESP Controller.

## The SleepUINO Pre-Development logo can be disabled or replaced by your logo
To disable/enable the logo, change the entry "logo" in ESPEasyFlasherConfig.json:
* Enable:

```json
"logo": true
```

* Disable: 

```json
"logo": false
```

If you want your own logo. Put the logo as png under the name "LogoEasyFlash.png" in the same directory as the ESPEasyFlasher.py or the executable if you use it as stand alone tool.

## Use ESPEasyFlasher_2.0 as python script
Requirements:
1. [python3](https://www.python.org/downloads/) has to be installed on your system
1. [esptool](https://pypi.org/project/esptool/) has to be installed as module. Under the [link]((https://pypi.org/project/esptool/)) you can find a description how you install the esptool in python. Short: ´pip install esptool´  

start the GUI as python script
1. python ESPEasyFlasher.py

## Try out ESPEasyFlasher_2.0 as executable from release directory
I have stored two zip files in the release v0.8-alpha as assets, to show how simple the ESPEasyFlasher is working. [ESPEasyFlasher_0.9.0_macOs.zip](https://github.com/hredan/ESPEASYFLASHER_2.0/releases/download/v0.8-alpha/ESPEasyFlasher_0.9.0_macOs.zip) you can use to test it on macOS [ESPEasyFlasher_0.9.0_win.zip](https://github.com/hredan/ESPEASYFLASHER_2.0/releases/download/v0.8-alpha/ESPEasyFlasher_0.9.0_win.zip) is for windows user. Unpack the zip on your operating systems. You can change the json file as described above. The zip contains also Blink.ino.d1_mini.bin as test firmware binary. This bin file is the compiled binary of example Blink.ino from ESP8266/Arduino. Try it out and check if the blue LED is blinking. This is very nice because you or your customer has do not install Arduino IDE or any other libraries. The ZIP File contains all what is needed to flash the ESP micro controller.

