# CharPi - Python HD44780 display driver for Raspberry Pi

Python character display (Hitachi HD44780) driver for Raspberry Pi with many features, such as automatic text alignment and Custom Output Handling (makes it easy to use intermediary chips such as Shift Registers), both coming in a future update. Includes support for I2C backpacks.

CharPi includes support for most character displays based on the Hitachi HD44780 display (including I2C backpacks). By default, it has support for displays with up to 4 rows, but this can be easily changed by modifying the Python list containing each row's starting DDRAM address.

Custom Output Handling makes it easy to use intermediary chips such as Shift Registers, or any other type of complex setups, by providing your own callback function that handles the output signals. Your function will be called by CharPi every time when a display command needs to be sent. Note that a display command is not necessarily equivalent to a CharPi function (meaning that if you call a function such as writeString(), your function will be called more than once). Your function will have an array as an argument. This array will store the pin values that will need to be sent to the display.

## Dependencies

CharPi relies on [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) and [smbus](https://pypi.org/project/smbus/) Python modules to communicate with the display. RPi.GPIO comes with the latest Raspberry Pi OS by default. SMBus isn't preinstalled on the Lite version, but you can install it with pip3. 

Python minimum tested version: 3.7.
Tested on Raspberry Pi OS Buster & Bullseye. It might work fine on other operating systems too (if the dependencies are installed and the required changes are made).


## Installation guide

To install CharPi, you'll first have to download this repository's code. You can use git to download it directly on the Pi.

Open the Terminal and navigate to the package's directory using:
```
cd Path_To_Package_Location/CharPi/code
```
Then, you can install the library using the following command (requires root privileges) :
```
sudo python3 setup.py install
```
You succesfully installed the library. Now you can start coding. Good luck on your projects!

## Display initialization

A display usually need be initialized using the number of rows and columns of the display.
However, in some cases, displays without an auxiliary chip might need to have a different initialization.
For example, an original HD44780 16x1 display probably needs to be initialized as an 8x2 display.

# Legal
Raspberry Pi is a trademark of Raspberry Pi Ltd.
This Python library is not affiliated with Raspberry Pi Ltd. in any way.
