import usb.core
import usb.util
import sys
import time

VENDOR_ID = 0x046d
PRODUCT_ID = 0xc900
LIGHT_OFF = 0x00
LIGHT_ON = 0x01

# export PYUSB_DEBUG=debug

dev = None
reattach = False


def init():
    global dev
    global reattach
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if dev.is_kernel_driver_active(0):
        print("kernel driver active")
        reattach = True
        dev.detach_kernel_driver(0)
    else:
        print("kernel driver not active")

    # was it found?
    if dev is None:
        raise ValueError('Device not found')

    # print(dev)

    dev.set_configuration()

    usb.util.claim_interface(dev, 0)


def cleanup():

    global dev
    global reattach
    usb.util.dispose_resources(dev)

    if reattach:
        dev.attach_kernel_driver(0)
        reattach = False


def light_on():
    global dev
    init()
    dev.write(0x02, [0x11, 0xff, 0x04, 0x1c, LIGHT_ON, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], 3000)
    dev.read(0x02, 64)
    print("Light On")
    cleanup()


def light_off():
    global dev
    init()
    dev.write(0x02, [0x11, 0xff, 0x04, 0x1c, LIGHT_OFF, 0x00, 0x00, 0x00, 0x00,
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], 3000)
    dev.read(0x02, 64)
    print("Light Off")
    cleanup()


def set_brightness(level):
    global dev
    init()
    dev.write(0x02, [0x11, 0xff, 0x04, 0x4c, 0x00, level, 0x00, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], 3000)
    dev.read(0x02, 64)
    print(f"Brightness {level}")
    cleanup()


def set_temperature(temp1, temp2):
    global dev
    init()
    dev.write(0x02, [0x11, 0xff, 0x04, 0x9c, temp1, temp2, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], 3000)
    dev.read(0x02, 64)
    print(f"Temperature {temp1}/{temp2}")
    cleanup()


light_on()
for i in range(0x14, 0x86, 10):
    set_brightness(i)
    time.sleep(1)
set_temperature(0x0a, 0x8c)  # Warm
time.sleep(3)
set_temperature(0x11, 0xf8)  # Medium
time.sleep(3)
set_temperature(0x19, 0x64)  # Cool
time.sleep(3)
set_brightness(0x14)
light_off()
