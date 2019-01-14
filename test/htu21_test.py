#!/usr/bin/env python3

from htu21 import HTU21

htu = HTU21()
print(htu.read_temperature())
print(htu.read_humidity())
