#!/usr/bin/env python3

import os
import time
import smbus

BUS = 1
ADDRESS = 0x62
MINLEVEL = 20

class Battery(object):

    def __init__(self):
        try:
            self.bus = smbus.SMBus(BUS)
            self.switch_battery_i2c_on()
        except:
            raise

    def switch_battery_i2c_on(self):
        try:
            battery_chip_state = self.bus.read_word_data(ADDRESS, 0x0A)
        except:
            raise
        else:
            if battery_chip_state == 0xC0:
                # print('BATTERY CHIP IS OFF\n\tself.battery_chip_state: ', self.battery_chip_state)
                # print('writing block data...')
                self.bus.write_byte_data(ADDRESS, 0x0A, 0x00)
                # print('block data was written.\nchecking state again...')
                # self.battery_chip_state = self.bus.read_word_data(ADDRESS, 0x0A)
                # print('BATTERY CHIP\n\tnew_self.battery_chip_state: ', self.battery_chip_state)
                time.sleep(0.5)
            elif battery_chip_state == 0x00:
                pass
            #     print('BATTERY CHIP IS ON\nself.battery_chip_state: ', self.battery_chip_state)
            else:
                raise ValueError('Battery I2C chip state is invalid: {}'.format(battery_chip_state))
            #     print('bty else pass')


    def _operation(self, operation, value):
        if operation == 'trimToTwo':
            return (value & 0xFFFF)
        elif operation == 'toggleMsbLsb':
            return (((value & 0xFF) << 8) | (value >> 8))
        elif operation == 'maskMSB':
            return (value & 0xFF00)
        elif operation == 'maskLSB':
            return (value & 0x00FF)

    def read_config(self):
        try:
            config = self._operation('trimToTwo', self.bus.read_word_data(ADDRESS, 0x00))
            return config
        except:
            pass

    def read_voltage(self):
        try:
            voltage = ((self._operation('toggleMsbLsb', self._operation('trimToTwo', self.bus.read_word_data(ADDRESS, 0x02)))) * 305) / 1000000
            return voltage
        except:
            pass

    def read_percentage(self):
        try:
            p = (self._operation('toggleMsbLsb', self._operation('trimToTwo', self.bus.read_word_data(ADDRESS, 0x04))))
            percentage = self._operation('toggleMsbLsb', self._operation('maskMSB', p)) + (self._operation('maskLSB', p) / 1000)
            return percentage
        except:
            pass

if __name__ == "__main__":
    battery = Battery()
    print('cfg: 0x{0:04X}'.format(battery.read_config()))
    print('voltage: ', battery.read_voltage(), 'V')
    print('percentage: ', battery.read_percentage(), '%')
