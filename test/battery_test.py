#! /usr/bin/env python3

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from terrarium import battery as Bty

DELAY = 60

battery = Bty.Battery()

# battery_chip_state = battery.battery_chip_state
# print('battery_chip_state: ', battery_chip_state)

cfg = battery.read_config()
print('cfg: 0x{0:04X}'.format(cfg))

# if self.battery_chip_state == 0xC0:
#     print('BATTERY CHIP IS OFF\n\tself.battery_chip_state: ', self.battery_chip_state)
#     print('writing a block...')
#     bus.write_block_data(ADDRESS, 0x0A, 0x00)
#     print('block written...\nchecking state again...')
#     self.battery_chip_state = self.bus.read_word_data(ADDRESS, 0x0A)
#     print('2.\tBATTERY CHIP IS OFF\nnew_self.battery_chip_state: ', self.battery_chip_state)
# elif self.battery_chip_state == 0x00:
#     print('BATTERY CHIP IS ON\nself.battery_chip_state: ', self.battery_chip_state)
# else:
#     print('bty else pass')






while True:
 v = battery.read_voltage()
 p = battery.read_percentage()
 print('{}%\t{}V'.format(p, v))
 time.sleep(DELAY)
