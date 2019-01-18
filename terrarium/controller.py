#!/usr/bin/env python3

import time
import RPi.GPIO as GPIO


try:
    from terrarium import _mcp23017 as _ctrl
    from terrarium import _dht_sensor as _dht_sensor
    from terrarium import _ds18b20_sensor as _ds18b20_sensor
    from terrarium import _bmx280_sensor as _bmx280_sensor
    from terrarium import _htu21_sensor as _htu21_sensor
except:
    raise

ctrl = _ctrl.MCP23017_ctrl()

class Tool(object):

    def __init__(self):
        self.ON = 0
        self.OFF = 1
        pass

    def switch_on(self):
        try:
            # GPIO.output(self.PIN, self.ON)
            ctrl.on(self.PIN, self.ON)
        except:
            raise

    def switch_off(self):
        try:
            # GPIO.output(self.PIN, self.OFF)
            ctrl.off(self.PIN, self.OFF)
        except:
            raise

    # def toggle(self):
    #     try:
    #         GPIO.output(self.PIN, self.ON) if GPIO.input(self.PIN) else GPIO.output(self.PIN, self.OFF)
    #     except:
    #         raise

    def state(self):
        try:
            # state = GPIO.input(self.PIN)
            state = ctrl.state()
            return state
        except:
            raise


class LAMP(Tool):

    def __init__(self, configuration):
        super().__init__()
        try:
            self.PIN = configuration["LAMP"]
        except Exception as e:
            self.PIN = 1


class UVB(Tool):

    def __init__(self, configuration):
        super().__init__()
        try:
            self.PIN = configuration['UVB']
        except Exception as e:
            self.PIN = 2


class HEATER(Tool):

    def __init__(self, configuration):
        super().__init__()
        try:
            self.PIN = configuration['HEATER']
        except Exception as e:
            self.PIN = 3


class RAIN(Tool):

    def __init__(self, configuration):
        super().__init__()
        try:
            self.PIN = configuration['RAIN']
        except Exception as e:
            self.PIN = 4




class REED_RELAY(object):

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
        return self.sensor.read()

class DHT_sensor(Sensor):

    def __init__(self, configuration):
        super().__init__()
        self.sensor = _dht_sensor.sensor(configuration)

class DS18B20_sensor(Sensor):

    def __init__(self):
        super().__init__()
        self.sensor = _ds18b20_sensor.sensor()

class BMx280_sensor(Sensor):

    def __init__(self, configuration):
        super().__init__()
        self.sensor = _bmx280_sensor.sensor(configuration)

class HTU21_sensor(Sensor):

    def __init__(self):
        super().__init__()
        self.sensor = _htu21_sensor.sensor()




class LED(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.OFF = 0
        self.ON = 1
        self.frequency = 100

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
            # for n in range(int(repeat)):
            #     GPIO.output(self.configuration[color], self.ON)
            #     time.sleep(0.3)
            #     GPIO.output(self.configuration[color], self.OFF)
            #     time.sleep(0.1)
            pausetime=0.01
            jump = 5
            color = GPIO.PWM(self.configuration[color], self.frequency)
            color.start(0)
            # time.sleep(3)
            print('pwm set. led: {}. start blinking.'.format(color))
            for n in range(int(repeat)):
                for i in range(0, 101, jump):
                    # print(i)
                    color.ChangeDutyCycle(i)
                    time.sleep(pausetime)
                for i in range(100, -1, -jump):
                    # print(i)
                    color.ChangeDutyCycle(i)
                    time.sleep(pausetime)
                time.sleep(0.5)
            color.stop()
        except:
            raise

    def all_off(self):
        try:
            pins = []
            for pin in self.configuration:
                pins.append(self.configuration[pin])
            GPIO.output(pins, 0)
        except Exception as e:
            raise
