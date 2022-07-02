# CharPi - Python HD44780 display driver for Raspberry Pi

Python character display (Hitachi HD44780) driver for Raspberry Pi with many features, such as automatic text alignment (coming in a future update). Includes support for I2C backpacks.

CharPi includes support for most character displays based on the Hitachi HD44780 display (including I2C backpacks). By default, it has support for displays with up to 4 rows, but this can be easily changed by changing the Python list that includes each row's starting DDRAM address when initializing the display or by using the RowAddresses list.


## Dependencies

CharPi relies on [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) and smbus Python modules that come with Raspberry Pi OS (tested on Buster & Bullseye) to communicate with the character display. However, many non-raspbian operating systems might work fine if the dependencies are installed and the required changes are made. Python minimum tested version: 3.7.


## Installation guide

To install CharPi, you'll first have to download one of the [releases](https://github.com/iCMDgithub/CharPi/releases).

Open the Terminal and navigate to the package's directory using:
```
cd Path_Inside_The_Package
```
Then, you can install the library using the following command (requires root privileges) :
```
sudo python3 setup.py install
```
You succesfully installed the library. Now you can start coding. Good luck on your projects!

## Display initialization
A display usually need be initialized using the number of rows and column of the display.
However, in some cases, displays without an auxiliary chip might need to have a different initialization.
For example, an original HD44780 16x1 display probably needs to be initialized as an 8x2 display.
