#! /usr/bun/env python3

import time
import RPi.GPIO as GPIO
import Adafruit_DHT as DHT

class sensor(object):

    def __init__(self, DHT_SENSOR):
        self.DHT_TYPE = DHT_SENSOR['DHT_TYPE']
        self.DHT_PIN = DHT_SENSOR['DHT_PIN']
       # self.DHT_RESET_PIN = DHT_SENSOR['DHT_RESET_PIN']
       # self.DHT_ERROR_THRESHOLD = DHT_SENSOR['DHT_ERROR_THRESHOLD']
       # self.DHT_ERROR_COUNT = 0

    def read(self):
        # print('Reading DHT{} sensor...'.format(self.DHT_TYPE))
        try:
            humidity, temperature = DHT.read_retry(self.DHT_TYPE, self.DHT_PIN)
            # if temperature is not None and humidity is not None:
                # self._reset_dht_error_counter()
           # else:
           #     self._dht_error(1)
           #  print("sensor: DHT{}\ttemperature: {}'C\thumidity: {}%\terror counter: {}".format(self.DHT_TYPE, temperature, humidity, self.DHT_ERROR_COUNT))
            return {'temperature' : temperature if temperature else -1,
                    'humidity' : humidity if humidity else -1}
        except:
            raise

    # def _dht_error(self, value):
    #     self.DHT_ERROR_COUNT += value
    #     # print('_dht_error\tcount: {}'.format(self.DHT_ERROR_COUNT))
    #     if self.DHT_ERROR_COUNT >= self.DHT_ERROR_THRESHOLD:
    #         self._reset_dht_sensor()
    #
    # def _reset_dht_sensor(self):
    #     try:
    #         GPIO.output(self.DHT_RESET_PIN, 0)
    #         time.sleep(0.5)
    #         GPIO.output(self.DHT_RESET_PIN, 1)
    #         # print('_reset_dht_sensor')
    #         self._reset_dht_error_counter()
    #     except:
    #         raise
    #
    # def _reset_dht_error_counter(self):
    #     self.DHT_ERROR_COUNT = 0
    #     # print('_reset_dht_error_counter')
