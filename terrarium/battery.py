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
        except:
            pass

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
            raise

    def read_voltage(self):
        try:
            voltage = round((((self._operation('toggleMsbLsb', self._operation('trimToTwo', self.bus.read_word_data(ADDRESS, 0x02)))) * 305) / 1000000), 3)
            return voltage
        except:
            raise

    def read_percentage(self):
        try:
            p = (self._operation('toggleMsbLsb', self._operation('trimToTwo', self.bus.read_word_data(ADDRESS, 0x04))))
            percentage = round(self._operation('toggleMsbLsb', self._operation('maskMSB', p)) + (self._operation('maskLSB', p) / 1000), 3)
            return percentage
        except:
            raise
