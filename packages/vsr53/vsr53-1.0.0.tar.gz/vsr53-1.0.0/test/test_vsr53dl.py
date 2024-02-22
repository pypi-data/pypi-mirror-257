from __future__ import annotations

import pytest

from vsr53 import VSR53DL
from vsr53.DisplayModes import Units
from vsr53.sys import dev_tty


@pytest.fixture()
def vacuum_sensor():
    sensor_address = 1
    vacuum_sense = VSR53DL(dev_tty, address=sensor_address)
    vacuum_sense.open_communication()
    yield vacuum_sense
    vacuum_sense.close_communication()


def test_device_query(vacuum_sensor):
    gauge = vacuum_sensor

    assert gauge.get_device_type() == "VSR205"
    assert gauge.get_product_name() == "VSR53DL"
    assert gauge.get_serial_number_device() == "20002583"
    assert gauge.get_serial_number_head() == "20002583"
    assert gauge.get_device_version() == 2.0
    assert gauge.get_firmware_version() == "0215"
    assert gauge.get_bootloader_version() == 2.0

    gauge.set_display_unit(Units.MBAR)
    assert gauge.get_display_unit() == Units.MBAR
