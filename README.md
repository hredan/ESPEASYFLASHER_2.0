![SleepUINO_Logo_PreDev](https://user-images.githubusercontent.com/48091357/111156537-25298a00-8596-11eb-8726-1fe5cd7bed93.png)

# Simple way to share your ESP ideas with a cross software GUI named ESPEasyFlahser_2.0 (EEF)
![EEF_CrossSoftware_3000ms](https://user-images.githubusercontent.com/48091357/123086748-1881c100-d424-11eb-9189-bef6e9a8bbd9.gif)

# EEF is a GUI written in python for the command line tool esptool

## Why I have implemented ESPEasyFlasher_2.0 (EEF)
I was searching for a simple tool to share firmware binaries for the DIY-Project SleepUINO. The [SleepUINO](https://github.com/hredan/SleepUino) is a alarm clock with a web interface based on an ESP8266.

What I have found was the command line tool [esptool.py](https://github.com/espressif/esptool) from espressif. It can be used to flash all ESP micro controller, it is a good base and the community is working on it. It is alive! And I have found some different GUIs. Some GUIs try to contain the whole functionality of the esptool and are very complex. I want a simple tool to share my firmware without any frills, like the [ESPEASYFLASHER](https://github.com/BattloXX/ESPEasyFlasher) from BattloXX. But this GUI is only usable on Windows. I want a GUI that is platform independently. So I have got ideas but I have not found a satisfactory solution.

## Build my own GUI based on esptool and tkinter called ESPEasyFlasher_2.0
I liked the simple usability of ESPEasyFlasher from BattloXX but I could not understand why it is implemented in C#. The esptool is not only a command line tool, it has also a python interface. Python itself is platform independently and contains tkinter, [a Python binding to the Tk GUI toolkit](https://en.wikipedia.org/wiki/Tkinter), as standard library. And the icing on the cake, with [pyinstaller](https://www.pyinstaller.org/) it is possible to generate executables for different os platforms. So why not implementing all things in Python and bring the idea of ESPEasyFlasher to the next level 2.0?

# Features of EEF
For more information about the ESPEasyFlasher_2.0 have a look to the [EEF Wiki](https://github.com/hredan/ESPEASYFLASHER_2.0/wiki). All functions are descripted there.

* EEF is a cross-platform software, because it is implemented as python script
* Customization without source code changes over an json file
* Using your own logo to share your ESP ideas 
* easy configuration of esptool parameter by eef files
* [Integrated Serial Monitor](https://github.com/hredan/ESPEASYFLASHER_2.0/wiki/Serial-Monitor)
* [Reset via RTS pins](https://github.com/hredan/ESPEASYFLASHER_2.0/wiki/Serial-Monitor#hard-resetting-of-the-esp-via-rts-pin)
* EEF Releases contains executable binaries for different platforms as examples, created with pyinstaller. You can take this examples with you own ESP binaries, customizing it, and share it with you Customers/Followers.

# Try it out!
It is very simple, what you need is an ESP8266 or ESP32. [Download the zip file for you specific platform](https://github.com/hredan/ESPEASYFLASHER_2.0/releases/latest). Unzip the file an start the executable.
The zip files contains 2 examples for an ESP8266 and the same 2 example for an ESP32
1. Blinking LED on ESP board
1. jQuery Web Interface to switch on/off the LED on the ESP board

# Disclaimer
All this code is released under the GPL, and all of it is to be used at your own risk. If you find any bugs, please let me know via the GitHub issue tracker or drop me an email ([hredan@sleepuino.info](mailto:hredan@sleepuino.info)).
