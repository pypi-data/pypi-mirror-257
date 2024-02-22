from __future__ import annotations

import logging

from vsr53 import VSR53USB
from vsr53.logger import log

if __name__ == "__main__":
    from vsr53.sys import dev_tty

    log.setLevel(logging.INFO)
    sensor_address = 1

    with VSR53USB(dev_tty, address=sensor_address) as gauge:
        gauge.get_device_type()
        gauge.get_product_name()
        gauge.get_serial_number_device()
        gauge.get_serial_number_head()
        gauge.get_device_version()
        gauge.get_firmware_version()
        gauge.get_measurement_value()
        gauge.get_measurement_value_piezo()
        gauge.get_measurement_value_pirani()
