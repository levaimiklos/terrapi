#!/usr/bin/env python3

try:
    from htu21 import HTU21 as HTU21

except Exception as e:
    raise

else:

    class sensor(object):

        def __init__(self):
            self.temperature = None
            self.humidity = None
            self.sensor = HTU21()

        def read(self):
            try:
                self.temperature = self.sensor.read_temperature()
                self.humidity = self.sensor.read_humidity()
            except Exception as e:
                raise
            finally:
                return {'temperature' : self.temperature,
                        'humidity' : self.humidity}
