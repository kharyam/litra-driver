"""
This module defines a library for accessing the functionality of the
Logitech Lumitra Glow
"""
import logging
import math
import usb.core
import usb.util
from llgd.config.llgd_config import LlgdConfig

VENDOR_ID = 0x046d
PRODUCT_ID = 0xc900
LIGHT_OFF = 0x00
LIGHT_ON = 0x01
TIMEOUT_MS = 3000
MIN_BRIGHTNESS = 0x14
MAX_BRIGHTNESS = 0xfa

config = LlgdConfig()

def count():

    devs = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID, find_all=True)
    total_dev_count = 0
    for _ in devs:
        total_dev_count+=1
    return total_dev_count

def setup(index):
    """Sets up the device

    Raises:
        ValueError: Whhen the device cannot be found

    Returns:
        [device, reattach]: where device is a Device object and reattach
        is a bool indicating whether the kernel driver should be reattached
    """
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        raise ValueError('Device not found')

    reattach = False

    try:
        if dev.is_kernel_driver_active(0):
            logging.debug("kernel driver active")
            reattach = True
            dev.detach_kernel_driver(0)
        else:
            logging.debug("kernel driver not active")

    except AttributeError:
        logging.debug(
            '"is_kernel_driver_active()" method not found. Continuing')

    logging.debug(dev)
    dev.set_configuration()
    usb.util.claim_interface(dev, 0)

    return dev, reattach


def teardown(dev, reattach):
    """Tears down the device
    """
    usb.util.dispose_resources(dev)
    if reattach:
        dev.attach_kernel_driver(0)


def light_on():
    """Turns on the light
    """
    dev, reattach = setup()
    dev.write(0x02, [0x11, 0xff, 0x04, 0x1c, LIGHT_ON, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], TIMEOUT_MS)
    dev.read(0x02, 64)
    logging.info("Light On")
    teardown(dev, reattach)


def light_off():
    """Turns off the light
    """
    dev, reattach = setup()
    dev.write(0x02, [0x11, 0xff, 0x04, 0x1c, LIGHT_OFF, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], TIMEOUT_MS)
    dev.read(0x02, 64)
    logging.info("Light Off")
    teardown(dev, reattach)


def set_brightness(level):
    """Sets the brightness level

    Args:
        level (int): The brigtness level from 1-100. Converted between the min and
        max brightness levels supported by the device.
    """
    dev, reattach = setup()
    adjusted_level = math.floor(
        MIN_BRIGHTNESS + ((level/100) * (MAX_BRIGHTNESS - MIN_BRIGHTNESS)))
    dev.write(0x02, [0x11, 0xff, 0x04, 0x4c, 0x00, adjusted_level, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], TIMEOUT_MS)
    dev.read(0x02, 64)
    config.update_current_state(brightness=level)
    logging.info("Brightness set to %d", level)
    teardown(dev, reattach)


def set_temperature(temp):
    """Sets the color temerpature

    Args:
        temp (int): A color temperature of between 2700 and 6500
    """
    dev, reattach = setup()
    byte_array = temp.to_bytes(2, 'big')
    dev.write(0x02, [0x11, 0xff, 0x04, 0x9c, byte_array[0], byte_array[1], 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
              TIMEOUT_MS)
    dev.read(0x02, 64)
    config.update_current_state(temp=temp)
    logging.info("Temperature set to %d", temp)
    teardown(dev, reattach)
