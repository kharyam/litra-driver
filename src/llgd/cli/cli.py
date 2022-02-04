"""
This module provides a command line interface (CLI) for accessing the functionality
of the Logitech Lumitra Glow
"""
import os
import logging
import fire
from llgd.lib.llgd_lib import light_on, light_off, set_brightness, set_temperature

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s', level=os.getenv('LITRA_LOGLEVEL',
                                                                      default='WARNING'))


class Cli():
    """CLI Implementation
    """

    def __init__(self):
        """Constructor
        """
        self.command_count = 0

    def on(self):  # pylint: disable=invalid-name
        """
        Turns on the Litra Glow
        """
        light_on()
        self.command_count += 1
        return self

    def off(self):
        """
        Turns off the Litra Glow
        """
        light_off()
        self.command_count += 1
        return self

    def bright(self, level):
        """
        Sets the brightness level of the Litra Glow
        :param level: level a brightness level in the range of 1-100
        """
        if level < 1 or level > 100:
            logging.warning("Brightness must be between 1 and 100")
        else:
            set_brightness(level)
        self.command_count += 1
        return self

    def temp(self, temp):
        """
        Sets the temperature level of the Litra Glow
        :param temp: Temperature to set the litra glow. Valid values are 2700 - 6500
        """
        if temp < 2700 or temp > 6500:
            logging.warning("Temperature must be between 2700 and 6500")
        else:
            set_temperature(temp)
        self.command_count += 1
        return self

    def __str__(self):
        count = self.command_count
        return f"Executed {count} commands"


def main():
    """Entrypoint into the cli
    """
    cli = Cli()

    # Explicitly map the commands to the class methods even though
    # they are identical. This allows the usage menu to only be
    # shown when no commands are specified.
    fire.Fire({
        'on': cli.on,
        'off': cli.off,
        'temp': cli.temp,
        'bright': cli.bright
    })


if __name__ == "__main__":
    main()
