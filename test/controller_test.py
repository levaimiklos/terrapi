#!/usr/bin/env python3

import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from terrarium import Configuration as Configuration
from terrarium import Controller as Controller

DELAY = 0.5

print('Starting Controller.py test.\n')

try:
    #LAMP
    # LAMP = Controller.LAMP(Configuration.TOOLS)
    # print('LAMP object: ', LAMP)
    # print('on state = ', LAMP.ON)
    # print('LAMP.state: ', LAMP.state())
    # LAMP.switch_on()
    # time.sleep(DELAY)
    # LAMP.switch_off()
    # time.sleep(DELAY)
    #
    # #HEATER
    # HEATER = Controller.Heater(Configuration.TOOLS)
    # print('HEATER object: ', HEATER)
    # print('on state = ', HEATER.ON)
    # print('HEATER.state: ', HEATER.state())
    # HEATER.switch_on()
    # time.sleep(DELAY)
    # HEATER.switch_off()
    # time.sleep(DELAY)
    #
    # #HUMIDIFIER
    # HUMIDIFIER = Controller.Humidifier(Configuration.TOOLS)
    # print('HUMIDIFIER object: ', HUMIDIFIER)
    # print('on state = ', HUMIDIFIER.ON)
    # print('HUMIDIFIER.state: ', HUMIDIFIER.state())
    # HUMIDIFIER.switch_on()
    # time.sleep(DELAY)
    # HUMIDIFIER.switch_off()
    # time.sleep(DELAY)
    #
    # #DEHUMIDIFIER
    # DEHUMIDIFIER = Controller.Dehumidifier(Configuration.TOOLS)
    # print('DEHUMIDIFIER object: ', DEHUMIDIFIER)
    # print('on state = ', DEHUMIDIFIER.ON)
    # print('DEHUMIDIFIER.state: ', DEHUMIDIFIER.state())
    # DEHUMIDIFIER.switch_on()
    # time.sleep(DELAY)
    # DEHUMIDIFIER.switch_off()
    # time.sleep(DELAY)
    #
    # #REED RELAY
    # Reed_relay = Controller.Reed_relay(Configuration.REED_RELAY)
    # print('Reed_relay object: ', Reed_relay)
    # print('Reed_relay.state: ', Reed_relay.state())
    #
    #
    # #DHT SENSOR
    # dht_sensor = Controller.DHT_sensor(Configuration.DHT_SENSOR1)
    # print('dht_sensor object: ', dht_sensor)
    # dht1_temp_humi_data = dht_sensor.read()
    # print('dht1_temp_humi_data: ', dht1_temp_humi_data)
    #
    # #DS18B20 SENSOR
    # ds18b20_sensor = Controller.DS18B20_sensor()
    # print('ds18b20_sensor object: ', ds18b20_sensor)
    # ds18b20_temp_humi_data = ds18b20_sensor.read()
    # print('ds18b20_temp_humi_data: ', ds18b20_temp_humi_data)

    #LED
    LED = Controller.LED(Configuration.LEDS)
    # time.sleep(1)
    # print('red')
    # LED.switch_on('RED_LED')
    # time.sleep(DELAY*2)
    # LED.switch_off('RED_LED')
    # time.sleep(DELAY)
    # print('green')
    # LED.switch_on('GREEN_LED')
    # time.sleep(DELAY*3)
    # LED.switch_off('GREEN_LED')
    # time.sleep(DELAY)
    # print('blue')
    # LED.switch_on('BLUE_LED')
    # time.sleep(DELAY*4)
    # LED.switch_off('BLUE_LED')
    # time.sleep(DELAY)

    LED.blink('RED_LED', 3)
    time.sleep(DELAY*2)
    LED.blink('GREEN_LED', 2)
    time.sleep(DELAY*2)
    LED.switch_on('BLUE_LED')
    time.sleep(DELAY*6)
    LED.switch_off('BLUE_LED')



except:
    raise
finally:
    # LED.all_off()
    pass
