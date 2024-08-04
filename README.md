# CharPi - Python HD44780 display driver for Raspberry Pi

<img src="/hello-CharPi.png" alt="Image of a display using CharPi">Python character display (Hitachi HD44780) driver for Raspberry Pi with special features such as Custom Output Handling (makes it easy to use intermediary chips such as Shift Registers). Includes support for I2C backpacks.

CharPi includes support for most character displays based on the Hitachi HD44780 display (including I2C backpacks). By default, it has support for displays with up to 4 rows, but this can be easily changed by modifying the Python list containing each row's starting DDRAM address.

## Special feature: Custom Output Handling
Custom Output Handling makes it easy to use intermediary chips such as Shift Registers, or any other type of complex setups, by providing your own callback function that handles the output signals. Your function will be called by CharPi every time a display command needs to be sent. Note that a display command is not necessarily equivalent to a CharPi function (meaning that if you call a function such as writeString(), your function will be called more than once). Your function will have a binary number as an argument. This argument will store the pin values that will need to be sent to the display, in the following format:

```
   | Digit 1 | Digit 2 | Digit 3 | Digit 4 |  Digit 5  | Digit 6 | Digit 7 | Digit 8 |
--------------------------------------------------------------------------------------
0b |  PIN 1  |  PIN 2  |  PIN 3  |  PIN 4  | BACKLIGHT |  none   |   RW    |   RS    |
```

The custom ouput handling object (HD44780CustomDriver()) uses the display in 4-bit mode.

Here is how your callback function should look like:
```
def functionName(binaryData):
    # send received data to the display
```

## Dependencies

CharPi relies on [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) (for GPIO) or [smbus](https://pypi.org/project/smbus/) (for I2C) Python modules to communicate with the display. Depending on how you're wiring the display, you may need to install one of these 2 modules. RPi.GPIO comes with the latest Raspberry Pi OS by default. SMBus isn't preinstalled on the Lite version, but you can install it with `pip3`. 

Python minimum tested version: 3.7.
Tested on Raspberry Pi OS Buster & Bullseye. It might work fine on other operating systems too (if the dependencies are installed and the required changes are made).


## Installation guide

To install CharPi, you can use PyPi:

```
pip3 install CharPi
```


## Usage

Check out the [examples](https://github.com/iCMDgithub/CharPi/tree/main/Examples).

## Display initialization

A display usually needs be initialized with its number of rows and columns.
However, in some cases, displays without an auxiliary chip might require a different initialization.
For example, an original HD44780 16x1 display might need to be initialized as an 8x2 display.

# Legal
Raspberry Pi is a trademark of Raspberry Pi Ltd.
This Python library is not affiliated with Raspberry Pi Ltd. in any way.
