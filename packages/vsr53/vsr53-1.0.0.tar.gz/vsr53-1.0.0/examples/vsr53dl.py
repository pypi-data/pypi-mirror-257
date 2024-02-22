from __future__ import annotations

import logging

from vsr53 import VSR53DL
from vsr53.DisplayModes import Orientation as Orientation
from vsr53.DisplayModes import Units as Units
from vsr53.logger import log

if __name__ == "__main__":
    from vsr53.sys import dev_tty

    log.setLevel(logging.INFO)
    sensor_address = 1

    with VSR53DL(dev_tty, address=sensor_address) as gauge:
        gauge.get_device_type()
        gauge.get_product_name()
        gauge.get_serial_number_device()
        gauge.get_serial_number_head()
        gauge.get_response_delay()
        gauge.get_device_version()
        gauge.get_firmware_version()
        gauge.get_bootloader_version()
        gauge.get_measurement_range()
        gauge.get_measurement_value()
        gauge.get_measurement_value_piezo()
        gauge.get_measurement_value_pirani()
        gauge.set_display_unit(Units.MBAR)
        gauge.get_display_unit()
        gauge.set_display_orientation(Orientation.NORMAL)
        gauge.get_display_orientation()
        gauge.get_relay_1_status()
        gauge.get_relay_2_status()
        gauge.get_operating_hours()
