#! /usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from terrarium import battery as Bty

battery = Bty.Battery()
cfg = battery.read_config()
print('cfg: 0x{0:04X}'.format(cfg))
v = battery.read_voltage()
print('v: {}'.format(v))
p = battery.read_percentage()
print('p: {}'.format(p))
