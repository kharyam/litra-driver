"""
This module provides a command line interface (CLI) for accessing the functionality
of the Logitech Lumitra Glow
"""
import os
import sys
import logging
import fire
from llgd.lib.llgd_lib import light_on, light_off, set_brightness, set_temperature

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', level=os.getenv('LITRA_LOGLEVEL'))


def power_on():
    """
    Turns on the Litra Glow
    """
    light_on()


def power_off():
    """
    Turns off the Litra Glow
    """
    light_off()


def brightness(level):
    """
    Sets the brightness level of the Litra Glow
    :param level: level a brightness level in the range of 1-100
    """
    if level < 1 or level > 100:
        print("Level must be between 1 and 100")
        sys.exit(1)
    set_brightness(level)


def temperature(temp):
    """
    Sets the temperature level of the Litra Glow
    :param temp: Temperature to set the litra glow. Valid values are 2700 - 6500
    """
    if temp < 2700 or temp > 6500:
        print("Level must be between 2700 and 6500")
        sys.exit(1)
    set_temperature(temp)


def main():
    """
    Define the CLI using fire
    """
    fire.Fire({
        "on": power_on,
        "off": power_off,
        "brightness": brightness,
        "temp": temperature
    })


def init():
    """
    Entrypoint into the CLI
    """

    if __name__ == "__main__":
        sys.exit(main())


init()
