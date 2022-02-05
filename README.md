# Python Utility for Logitech Litra Glow

## Introduction

After purchasing a [Logitech Litra Glow](https://www.logitech.com/en-us/products/lighting/litra-glow.946-000001.html) I was unable to find any support for linux. This project reverse-engineers the basic functionality of the litra pro so that we can control it via USB without using the physical buttons on the device.

## Quick Start

### Linux
```bash
# If necessary, create a udev role to grant permission to access the light
sudo echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="046d", ATTR{idProduct}=="c900",\
           MODE="0666"' > /etc/udev/rules.d/82-litra-glow.rules

sudo reboot

# Uninstall if previously installed
pip uninstall litra-driver
pip install litra-driver

# Command Line Interface
lc --help

# User Interface
lcui

```

## The UI
A basic UI can be launched to allow control of the light:

```bash
lcui
```

![lcui Screen Shot](images/ui.png)
## The CLI

The log level can be adjusted by setting the environment variable `LITRA_LOGLEVEL` to one of the following:
* CRITICAL
* ERROR
* WARNING
* INFO
* DEBUG

```
NAME
    lc

SYNOPSIS
    lc COMMAND

COMMANDS
    COMMAND is one of the following:

     on
       Turns on the Litra Glow

     off
       Turns off the Litra Glow

     temp
       Sets the temperature level of the Litra Glow

     bright
       Sets the brightness level of the Litra Glow
```

Sample Usage
```bash
lc on
lc brightness 1
lc brightness 50
lc off

# Chain multiple commands
lc on brightness 100 temperature 2700
```

## Development
### Creating / installing the distribution

```bash
# Create distribution
python -m build

# Local Testing
pip install --editable .

# Linter
tox -e lint

# Unit Test - "Coming Soon"™
tox -e test
```
