#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO
from terrarium import _dht_sensor as _dht_sensor
from terrarium import _ds18b20_sensor as _ds18b20_sensor


class Tool(object):

    def __init__(self):
        self.ON = 0
        self.OFF = 1
        pass

    def switch_on(self):
        try:
            GPIO.output(self.PIN, self.ON)
        except:
            raise

    def switch_off(self):
        try:
            GPIO.output(self.PIN, self.OFF)
        except:
            raise

    def toggle(self):
        try:
            GPIO.output(self.PIN, self.ON) if GPIO.input(self.PIN) else GPIO.output(self.PIN, self.OFF)
        except:
            raise

    def state(self):
        try:
            state = GPIO.input(self.PIN)
            return state
        except:
            raise


class Lamp(Tool):

    def __init__(self, configuration):
        super().__init__()
        self.PIN = configuration['LAMP']


class Heater(Tool):

    def __init__(self, configuration):
        super().__init__()
        self.PIN = configuration['HEATER']


class Humidifier(Tool):

    def __init__(self, configuration):
        super().__init__()
        self.PIN = configuration['HUMIDIFIER']


class Dehumidifier(Tool):

    def __init__(self, configuration):
        super().__init__()
        self.PIN = configuration['DEHUMIDIFIER']




class Reed_relay(object):

    def __init__(self, configuration):
        self.PIN = configuration['REED_RELAY']

    def state(self):
        try:
            state = GPIO.input(self.PIN)
            return state
        except:
            raise




class Sensor(object):

    def __init__(self):
        pass

    def read(self):
        print('Read.')
        return self.sensor.read()

class DHT_sensor(Sensor):

    def __init__(self, configuration):
        super().__init__()
        self.sensor = _dht_sensor.sensor(configuration)

class DS18B20_sensor(Sensor):

    def __init__(self):
        super().__init__()
        self.sensor = _ds18b20_sensor.sensor()

class BMP280_sensor(Sensor):

    def __init__(self):
        super().__init__()
        self.sensor = _bmp280_sensor.sensor()




class LED(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.OFF = 0
        self.ON = 1

    def switch_on(self, color):
        try:
            GPIO.output(self.configuration[color], self.ON)
        except:
            raise

    def switch_off(self, color):
        try:
            GPIO.output(self.configuration[color], self.OFF)
        except:
            raise

    def blink(self, color, repeat):
        try:
            for n in range(int(repeat)):
                GPIO.output(self.configuration[color], self.ON)
                time.sleep(0.3)
                GPIO.output(self.configuration[color], self.OFF)
                time.sleep(0.1)
        except:
            raise
