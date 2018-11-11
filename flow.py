#!/usr/bin/env python3

import os
import threading
import time
import json
import atexit
# import logging

import RPi.GPIO as GPIO
import Adafruit_DHT as DHT

#imports from own package
import terrarium as Terrarium
from terrarium import Configuration
from terrarium import Scheduler as Scheduler
from terrarium import Battery as Battery
from terrarium import Controller as Controller

"""Create a logger"""
# date_now = time.strftime("%Y%m%d_%H%M")
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%y/%m/%d %H:%M:%S',
#                     filename='/home/pi/terrapi/log/log_' + date_now + '.log',
#                     filemode='a')
# terrarium_logger = logging.getLogger('TerraPI')


"""Make sure RPI.GPIO resources are cleaned up at the end of the program."""
atexit.register(GPIO.cleanup)


"""check the pin init success"""
pin_init_success = 1 if Terrarium.pin_init_success else sys.exit(69)

"""Initiating the objects"""
Lamp = Controller.Lamp(Configuration.TOOLS)
Heater = Controller.Heater(Configuration.TOOLS)
Humidifier = Controller.Humidifier(Configuration.TOOLS)
Dehumidifier = Controller.Dehumidifier(Configuration.TOOLS)
DHT_sensor_1 = Controller.DHT_sensor(Configuration.DHT_SENSOR1)
Reed_relay = Controller.Reed_relay(Configuration.REED_RELAY)
LED = Controller.LED(Configuration.LEDS)

class Flow(object):

    def __init__(self):
        self.DELAY = Configuration.TIMING['delay']

        self.temperature = None
        self.set_temperature = float(Configuration.CONTROLLER['set_temperature'])
        self.new_temperature_setpoint = self.set_temperature
        self.temperature_threshold = int(Configuration.CONTROLLER['temperature_threshold'])

        self.humidity = None
        self.set_humidity = float(Configuration.CONTROLLER['set_humidity'])
        self.new_humidity_setpoint = self.set_humidity
        self.humidity_threshold = int(Configuration.CONTROLLER['humidity_threshold'])
        self.max_humidity = int(Configuration.CONTROLLER['max_humidity'])

        self.heater_state = Heater.OFF  # Heating is OFF by default
        self.humidifier_state   = Humidifier.OFF  # Humidifying is OFF by default
        self.dehumidifier_state = Dehumidifier.OFF  # Dehumidifying is OFF by default

        """LOCK"""
        self._lock = threading.Lock()
        self._lamp_lock = threading.Lock()

        """CALLBACKS"""
        self._door_callback = None
        self._dht_callback = None
        self._lamp_callback = None
        self._heater_callback = None
        self._humidifier_callback = None
        self._dehumidifier_callback = None

        #setup RPi.GPIO to fire an internal callback when the door changes state
        GPIO.add_event_detect(Configuration.REED_RELAY['REED_RELAY'], GPIO.BOTH, callback=self._door_change, bouncetime=100)

        """"THREADS"""
        # Create and start DHT reading thread in the background
        self._dht_thread = threading.Thread(target=self._update_dht, name = "_dht_thread", daemon = True)
        self._dht_thread.start()
        # self._dht_thread_ident = self._dht_thread.ident
        #Create and start light switching thread in the background
        self._lamp_thread = threading.Thread(target=self._switch_lamp, name="_lamp_thread", daemon = True)
        self._lamp_thread.start()
        # self._lamp_thread_ident = self._lamp_thread.ident
        # self.active_threads = threading.active_count()
        #Create a log entry of the threads
        # terrarium_logger.debug('Number of active threads: %s.\t%s ident: %s.\t%s ident: %s.', self.active_threads, self._dht_thread.name, self._dht_thread_ident, self._lamp_thread.name, self._lamp_thread_ident)


    """BACKGROUND THREAD functions"""
    #switch the daylight lamp as per the scheduler
    def _switch_lamp(self):
        while True:
            with self._lamp_lock:
                if Scheduler.is_light_time():
                    Lamp.switch_on() #ON
                    if self._lamp_callback is not None:
                        self._lamp_callback(Lamp.state())
                    print('LAMP: ON')
                else:
                    Lamp.switch_off() #OFF
                    if self._lamp_callback is not None:
                        self._lamp_callback(Lamp.state())
                    print('LAMP: OFF')
                # terrarium_logger.debug('LAMP is ON') if not GPIO.input(int(configuration['TOOLS']['LAMP'])) else terrarium_logger.debug('LAMP is OFF')
            time.sleep(self.DELAY)

    #update the temperature and humidity values in every 'delay' seconds
    def _update_dht(self):
        """Main function for DHT update thread, will grab new temp & humidity values every n seconds."""
        while True:
            with self._lock:
                # Read the humidity and temperature from the DHT sensor.
                data = DHT_sensor_1.read()
                self.temperature = round(data['temperature'], 2)
                self.humidity = round(data['humidity'], 2)
                if self._dht_callback is not None:
                    self._dht_callback(self.temperature, self.humidity)
                self.check_temperature(self.temperature)
                self.check_humidity(self.humidity)
                LED.blink('GREEN_LED', 2) if data['temperature'] is not 0 and data['humidity'] is not 0 else LED.blink('RED_LED', 4)
            print("TEMPERATURE: {}'C,\tHUMIDITY: {}%,\tDATE: {}.".format(data['temperature'], data['humidity'], time.strftime("%Y.%m.%d., %H:%M:%S")))
            # terrarium_logger.info("TEMPERATURE: %s'c,\tHUMIDITY: %s\tDATE: %s ", temperature, humidity, time.strftime("%Y.%m.%d., %H:%M:%S"))
            time.sleep(self.DELAY)


    """SOCKET TRIGGERS"""
    def on_temp_humidity_change(self, callback):
        self._dht_callback = callback
    def on_door_change(self, callback):
        self._door_callback = callback
    def on_lamp_change(self, callback):
        self._lamp_callback = callback
    def on_heater_change(self, callback):
        self._heater_callback = callback
    def on_humidifier_change(self, callback):
        self._humidifier_callback = callback
    def on_dehumidifier_change(self, callback):
        self._dehumidifier_callback = callback


    """"REED RELAY"""
    def _door_change(self, pin):
        # Called by the RPI.GPIO library when the door pin changes state.
        # Check if someone has registered a thing door callback and call it with the current thing door state.
        if self._door_callback is not None:
            self._door_callback(Reed_relay.state())
        # terrarium_logger.debug('DOOR state is %s', GPIO.input(int(configuration["REED_RELAY"]["REED_RELAY"])))

    def read_door(self):
        # Read the door state and return it's current value.
        with self._lock:
            return Reed_relay.state()


    """"LAMP"""
    def read_lamp(self):
        # Read the lamp state and return its current value.
        with self._lock:
            return Lamp.state()


    """LED"""
    def set_led(self, value):
        #Set the RED LED (On = True, Off = False)
        with self._lock:
            LED.switch_on('BLUE_LED') if value else LED.switch_off('BLUE_LED')


    """TEMPERATURE"""
    def check_temperature(self, temperature):
        if Scheduler.is_light_time():
            if 17 < temperature < 40:
                if temperature <= (self.new_temperature_setpoint - self.temperature_threshold):
                    if self.heater_state == Heater.OFF and Heater.state():
                        Heater.switch_on()
                        self.heater_state = Heater.state()
                        self._trigger_heater_callback()
                elif temperature >= (self.new_temperature_setpoint + self.temperature_threshold):
                    if self.heater_state == Heater.ON and not Heater.state():
                        Heater.switch_off()
                        self.heater_state = Heater.state()
                        self._trigger_heater_callback()
                elif ((self.new_temperature_setpoint - self.temperature_threshold) < temperature < (self.new_temperature_setpoint + self.temperature_threshold)):
                    # print('Temperature is in the range, no action was taken.')
                    pass
                else:
                    # ERROR while checking the temperature.
                    Heater.switch_off()
                    self.heater_state = Heater.state()
                    self._trigger_heater_callback()
                    # terrarium_logger.error('ERROR with TEMPERATURE: %s', temperature)
            else:
                # terrarium_logger.error('TEMPERATURE is: %s - out of range', temperature)
                pass
        else:
            # Not heating, out of timeframe.
            Heater.switch_off()
            self.heater_state = Heater.state()
            self._trigger_heater_callback()
        print('end of temp checking func.')

    def increase_temperature_setpoint(self, value):
        new_value = self.new_temperature_setpoint + value
        self.new_temperature_setpoint = round(new_value, 2)
        print('new_temperature_setpoint: ', self.new_temperature_setpoint)
        # terrarium_logger.debug('Temperature setpoint was increased. New value: %s', self.new_temperature_setpoint)
        return self.new_temperature_setpoint

    def decrease_temperature_setpoint(self, value):
        new_value = self.new_temperature_setpoint - value
        self.new_temperature_setpoint = round(new_value, 2)
        print('new_temperature_setpoint: ', self.new_temperature_setpoint)
        # terrarium_logger.debug('Temperature setpoint was decreased. New value: %s', self.new_temperature_setpoint)
        return self.new_temperature_setpoint

    def read_heater(self):
        #Read the heater state and return its current value.
        with self._lock:
            return Heater.state()

    # Callback trigger on change
    def _trigger_heater_callback(self):
        if self._heater_callback is not None:
            self._heater_callback(self.heater_state)


    """HUMIDITY"""
    def check_humidity(self, humidity):
        if 10 < humidity < 99:
            if humidity < (self.new_humidity_setpoint - self.humidity_threshold):
                Humidifier.switch_on()
                Dehumidifier.switch_off()
                self.humidifier_state = Humidifier.state()
                self.dehumidifier_state = Dehumidifier.state()
                self._trigger_humidifier_callback()
                self._trigger_dehumidifier_callback()
            elif ((self.new_humidity_setpoint - self.humidity_threshold) <= humidity < (self.new_humidity_setpoint + self.humidity_threshold)):
                if (self.humidifier_state == Humidifier.ON and not Humidifier.state()) or (self.humidifier_state == Humidifier.OFF and Humidifier.state()): #ON & ON  or  OFF & OFF
                    # print('No change in humidifier. It is ON or OFF already.')
                    pass
                else:
                    Humidifier.switch_on()
                    Dehumidifier.switch_off()
            elif ((self.new_humidity_setpoint + self.humidity_threshold) <= humidity < (self.max_humidity-5)):
                Humidifier.switch_off()
                Dehumidifier.switch_off()
                self.humidifier_state = Humidifier.state()
                self.dehumidifier_state = Dehumidifier.state()
                self._trigger_humidifier_callback()
                self._trigger_dehumidifier_callback()
            elif ((self.max_humidity-5) <= humidity < (self.max_humidity+5)):
                if (self.humidifier_state == Humidifier.ON and not Humidifier.state()) or (self.humidifier_state == Humidifier.OFF and Humidifier.state()): #ON & ON  or  OFF & OFF
                    # print('No change in dehumidifier. It is ON or OFF already.')
                    pass
                else:
                    Humidifier.switch_off()
                    Dehumidifier.switch_on()
                    self.humidifier_state = Humidifier.state()
                    self.dehumidifier_state = Dehumidifier.state()
                    self._trigger_humidifier_callback()
                    self._trigger_dehumidifier_callback()
            elif (self.max_humidity+5) <= humidity:
                Humidifier.switch_off()
                Dehumidifier.switch_on()
                self.humidifier_state = Humidifier.state()
                self.dehumidifier_state = Dehumidifier.state()
                self._trigger_humidifier_callback()
                self._trigger_dehumidifier_callback()
            else:
                Humidifier.switch_off()
                Dehumidifier.switch_off()
                self.humidifier_state = Humidifier.state()
                self.dehumidifier_state = Dehumidifier.state()
                self._trigger_humidifier_callback()
                self._trigger_dehumidifier_callback()
                # terrarium_logger.error('ERROR with humidity: %s ' %humidity)
        else:
            # terrarium_logger.error('Humidity is: %s - out of range', humidity)
            pass

    def increase_humidity_setpoint(self, value):
        new_value = self.new_humidity_setpoint + value
        self.new_humidity_setpoint = round(new_value, 2)
        print('new_humidity_setpoint: ', self.new_humidity_setpoint)
        # terrarium_logger.debug('Humidity setpoint was increased. New value: %s', self.new_humidity_setpoint)
        return self.new_humidity_setpoint

    def decrease_humidity_setpoint(self, value):
        new_value = self.new_humidity_setpoint - value
        self.new_humidity_setpoint = round(new_value, 2)
        print('new_humidity_setpoint: ', self.new_humidity_setpoint)
        # terrarium_logger.debug('Humidity setpoint was decreased. New value: %s', self.new_humidity_setpoint)
        return self.new_humidity_setpoint

    def read_humidifier(self):
        """Read the humidifier state and return its current value."""
        with self._lock:
            return Humidifier.state()

    def read_dehumidifier(self):
        """Read the humidifier state and return its current value."""
        with self._lock:
            return Dehumidifier.state()

    # Callback trigger on change
    def _trigger_humidifier_callback(self):
        # Callback trigger on change
        if self._humidifier_callback is not None:
            self._humidifier_callback(self.humidifier_state)

    # Callback trigger on change
    def _trigger_dehumidifier_callback(self):
        # Callback trigger on change
        if self._dehumidifier_callback is not None:
            self._dehumidifier_callback(self.dehumidifier_state)

    """"BATTERY"""
    def read_battery_percentage(self):
        # Read the battery percentage and return its current value.
        return Battery.read_percentage()

    def read_battery_voltage(self):
        # Read the battery percentage and return its current value.
        return Battery.read_voltage()




if __name__ == "__main__":
    print("Press CTRL+C fo finish.")
    Flow()
    while True:
        pass
