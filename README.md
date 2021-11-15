# CharPi - Python HD44780 display driver for Raspberry Pi
Python character display (Hitachi HD44780) driver for Raspberry Pi with many features, such as automatic text alignment. Includes support for I2C backpacks.

CharPi includes support for most character displays based on the Hitachi HD44780 display (including I2C backpacks; upcoming 74HC595 support in the following update). By default, it has support for displays with up to 4 rows, but this can be easily changed by changing the Python list that includes each row's starting DDRAM address when initializing the display or by using the RowAddresses list.

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
