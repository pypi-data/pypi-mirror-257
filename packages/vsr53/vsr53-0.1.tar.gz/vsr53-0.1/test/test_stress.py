from __future__ import annotations

import csv
import logging
from datetime import datetime

from vsr53 import VSR53DL
from vsr53.logger import log

log.setLevel(logging.ERROR)


def get_now_timestamp_str() -> str:
    now = datetime.now()
    return now.strftime("%m%d%Y%H%M%S")


def open_file(filename: str) -> csv.writer:
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Run", "Measurement", "Time Stamp"])
        return writer


def perform_measurement(vacuum_sense: VSR53DL, writer: csv.writer):
    for run in range(100000000):
        measurement = vacuum_sense.get_measurement_value()
        print(f"RUN #{run} measurement: {measurement}mbar")
        writer.writerow([run, measurement, get_now_timestamp_str()])


def stress_test():
    from vsr53.sys import dev_tty

    sensor_address = 1
    with VSR53DL(dev_tty, address=sensor_address) as gauge:
        filename = f"./results/Stress_test_results_{get_now_timestamp_str()}.csv"
        writer = open_file(filename)
        perform_measurement(gauge, writer)


if __name__ == "__main__":
    stress_test()
