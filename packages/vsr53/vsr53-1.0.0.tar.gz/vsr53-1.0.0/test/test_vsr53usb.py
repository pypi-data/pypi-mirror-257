from __future__ import annotations

import pytest

from vsr53 import VSR53USB
from vsr53.sys import dev_tty


@pytest.fixture()
def vacuum_sensor():
    sensor_address = 1
    vacuum_sense = VSR53USB(dev_tty, address=sensor_address)
    vacuum_sense.open_communication()
    yield vacuum_sense
    vacuum_sense.close_communication()


def test_device_query(vacuum_sensor):
    gauge = vacuum_sensor

    assert gauge.get_device_type() == "VSR213"
    assert gauge.get_product_name() == "VSR53USB"
    assert gauge.get_serial_number_device() == "22002816"
    assert gauge.get_serial_number_head() == "22002816"
    assert gauge.get_device_version() == 2.0
    assert gauge.get_firmware_version() == "0003"
