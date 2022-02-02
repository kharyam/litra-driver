# Python Utility for Logitech Litra Glow

## Introduction

After purchasing a [Logitech Litra Glow](https://www.logitech.com/en-us/products/lighting/litra-glow.946-000001.html) I was unable to find any support for linux. This project attempts to reverse-engineer the basic functionality of the litra pro so that we can control it via USB without using the physical buttons on the device.

## Current Status

Successfully reverse engineered USB calls to turn on / off the device, set the brightness and set the temperature. The code is currently just a demo of this functionality using [PyUSB](https://pyusb.github.io/pyusb/).  This will be expanded to a simple CLI / UI that can be used to control a litra.

## Running the demo (Linux)

This has been tested on Fedora 35

```bash
sudo echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="046d", ATTR{idProduct}=="c900", MODE="0666"' \
      > /etc/udev/rules.d/82-litra-glow.rules

git clone https://github.com/kharyam/litra-driver.git

cd litra-driver

python -m venv .venvs/default
source .venvs/default/bin/activate
pip install pyusb
python litra-demo.py
```

