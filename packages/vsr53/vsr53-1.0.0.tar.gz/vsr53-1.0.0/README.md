# [VSR53](https://github.com/lobis/vsr53)

[![PyPI version](https://badge.fury.io/py/vsr53.svg)](https://badge.fury.io/py/vsr53)

[![Build and Test](https://github.com/lobis/vsr53/actions/workflows/build.yaml/badge.svg)](https://github.com/lobis/vsr53/actions/workflows/build.yaml)

This is a Python library to communicate with
[Thyracont](https://thyracont-vacuum.com/en/)'s VSR53USB pressure gauge. It
should also work with the VSR53DL model (over RS485) but I haven't tested it as
I don't have access to one.

This library is a fork of
[this repository](https://github.com/IFAEControl/pyvsr53dl). All credits go to
the original author.

The original library was designed for the RS485 protocol and does not work out
of the box for the USB version of this sensor, however, with some minor
modifications such as allowing the user to set the baudrate and updating the
default value (to 9600 instead of 115200) it works perfectly.

## Installation

This library is [available in PyPI](https://pypi.org/project/vsr53/) and can be
installed with pip:

```bash
pip install vsr53
```

## Usage

```python
from vsr53 import VSR53USB

port = "/dev/ttyUSB0"  # replace with the device port of your gauge
with VSR53USB(port) as gauge:
    print(gauge.get_device_type())
    print(gauge.get_product_name())
    print(gauge.get_measurement_value())
```
