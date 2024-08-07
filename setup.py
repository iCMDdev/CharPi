from setuptools import setup

__name__ = "CharPi"
__version__ = "0.2.6"
__description__ = "Alpha version. This module is a driver for HD4480 and HD4480-like LCDs."
__packages__ = ["CharPi"]
__author__ = "github.com/iCMDdev"
__url__ = "https://www.github.com/iCMDdev/CharPi"
__download_url = 'https://github.com/iCMDdev/CharPi/archive/refs/tags/v0.2.6.tar.gz'
__keywords__ = ["HD44780", "I2C", "LCD", "display", "character"]
__requires__ = ["RPi.GPIO", "smbus"]

__classifiers__ = [
    "Development Status :: 3 - Alpha",
    'Intended Audience :: Developers',
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Programming Language :: Python :: 3",
    "Topic :: System :: Hardware"
]

setup(
    name = __name__,
    version = __version__,
    description = __description__,
    packages = __packages__,
    author = __author__,
    url = __url__,
    classifiers = __classifiers__,
    keywords = __keywords__,
    requires = __requires__,
)
