from __future__ import annotations

import platform

if platform.system() == "Darwin":
    dev_tty = "/dev/cu.usbserial-FT4VOTGK"
elif platform.system() == "Windows":
    dev_tty = "COM5"
elif platform.system() == "Linux":
    dev_tty = "/dev/ttyUSB0"
