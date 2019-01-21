#!/usr/bin/env python3

import os
import threading
import time
import json
import atexit
# import logging
import RPi.GPIO as GPIO

#imports from own package
import terrarium as Terrarium
from terrarium import Configuration as Configuration
from terrarium import Scheduler as Scheduler
from terrarium import Battery as Battery
from terrarium import Controller as Controller
from terrarium import IFTTT as IFTTT


"""Create a logger"""
# date_now = time.strftime("%Y%m%d_%H%M")
# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
#                     datefmt='%y/%m/%d %H:%M:%S',
#                     filename='/home/pi/terrapi/log/log_' + date_now + '.log',
#                     filemode='a')
# terrarium_logger = logging.getLogger('TerraPI')


# """check the pin init success"""
# pin_init_success = 1 if Terrarium.pin_init_success else sys.exit(69)


"""Initiating the objects"""
LAMP = Controller.LAMP(Configuration.TOOLS)
UVB = Controller.UVB(Configuration.TOOLS)
HEATER = Controller.HEATER(Configuration.TOOLS)
RAIN = Controller.RAIN(Configuration.TOOLS)
REED_RELAY = Controller.REED_RELAY(Configuration.REED_RELAY)
LED = Controller.LED(Configuration.LEDS)
BATTERY = Battery.Battery()

#__SENSORS__
Sensor_1 = Controller.DHT_sensor(Configuration.DHT_SENSOR1)
# Sensor_1 = Controller.DS18B20_sensor()
# Sensor_1 = Controller.BMx280_sensor(Configuration.BMx_SENSOR)
# Sensor_1 = Controller.HTU21_sensor()

# Sensor_2 = Controller.DHT_sensor(Configuration.DHT_SENSOR2)
# Sensor_2 = Controller.DS18B20_sensor()
Sensor_2 = Controller.BMx280_sensor(Configuration.BMx_SENSOR)
# Sensor_2 = Controller.HTU21_sensor()


"""Make sure RPI.GPIO resources are cleaned up at the end of the program."""
def exit_proc():
    print('exiting')
    LED.blink('BLUE_LED', 5)
    LAMP.switch_off()
    UVB.switch_off()
    HEATER.switch_off()
    RAIN.switch_off()
    GPIO.cleanup()
    print('bye...')

atexit.register(exit_proc)



class Flow(object):

    def __init__(self):
        self.DELAY = Configuration.TIMING['delay']
        self.temperature1 = None
        self.temperature2 = None
        self.set_temperature = float(Configuration.CONTROLLER['set_temperature'])
        self.new_temperature_setpoint = self.set_temperature
        self.temperature_threshold = int(Configuration.CONTROLLER['temperature_threshold'])
        self.humidity1 = None
        self.humidity2 = None
        self.LAMP_state = LAMP.switch_off()
        self.UVB_state = UVB.switch_off()
        self.HEATER_state   = HEATER.switch_off()
        # self.RAIN_state = RAIN.switch_off()
        self.RAIN_state = 1
        self.battery_warning_count = 0


        """LOCK"""
        self._lock = threading.Lock()
        self._TIMER_lock = threading.Lock()

        """CALLBACKS"""
        self._door_callback = None
        self._temphumi_callback = None
        self._temphumi2_callback = None
        self._LAMP_callback = None
        self._UVB_callback = None
        self._HEATER_callback = None
        self._RAIN_callback = None
        self._BATTERY_callback = None

        #setup RPi.GPIO to fire an internal callback when the door changes state
        GPIO.add_event_detect(Configuration.REED_RELAY['REED_RELAY'], GPIO.BOTH, callback=self._door_change, bouncetime=100)

        """"THREADS"""
        # Create and start DHT reading thread in the background
        self._temphumi_thread = threading.Thread(target=self._update_temphumi, name = "_temphumi_thread", daemon = True)
        self._temphumi_thread.start()
        self._timer_thread = threading.Thread(target=self._timer, name="_timer_thread", daemon = True)
        self._timer_thread.start()
        self._battery_thread = threading.Thread(target=self._update_battery, name="_battery_thread", daemon = True)
        self._battery_thread.start()


    """BACKGROUND THREAD functions"""
    #switch the daylight LAMP as per the scheduler
    def _timer(self):
        while True:
            with self._TIMER_lock:
                if Scheduler.is_light_time():
                    LAMP.switch_on() #ON
                    self.LAMP_state = LAMP.ON
                    if self._LAMP_callback is not None:
                        self._LAMP_callback(self.LAMP_state)
                    print('LAMP: ON')
                else:
                    LAMP.switch_off() #OFF
                    self.LAMP_state = LAMP.OFF
                    if self._LAMP_callback is not None:
                        self._LAMP_callback(self.LAMP_state)
                    print('LAMP: OFF')
            with self._TIMER_lock:
                if Scheduler.is_UVB_time():
                    UVB.switch_on()
                    self.UVB_state = UVB.ON
                    if self._UVB_callback is not None:
                        self._UVB_callback(self.UVB_state)
                    print('UVB: ON')
                else:
                    UVB.switch_off()
                    self.UVB_state = UVB.OFF
                    if self._UVB_callback is not None:
                        self._UVB_callback(self.UVB_state)
                    print('UVB: OFF')
            # terrarium_logger.debug('LAMP is ON') if not GPIO.input(int(configuration['TOOLS']['LAMP'])) else terrarium_logger.debug('LAMP is OFF')
            time.sleep(5)

    #update the temperature and humidity values in every 'delay' seconds
    def _update_temphumi(self):
        """Main function for _update_temphumi thread, will grab new temp & humidity values every 'delay' seconds."""
        while True:
            with self._lock:
                # Read the humidity and temperature from the DHT sensor.
                try:
                    data1 = Sensor_1.read()
                except Exception as e:
                    raise
                else:
                    self.temperature1 = round(data1['temperature'], 3)
                    self.humidity1 = round(data1['humidity'], 3)
                    if self._temphumi_callback is not None:
                        self._temphumi_callback(self.temperature1, self.humidity1)
                    self.check_temperature(self.temperature1, self.humidity1)
                    print("___DATA_1___\n\tTEMPERATURE: {}'C,\tHUMIDITY: {}%,\tDATE: {}.".format(data1['temperature'], data1['humidity'], time.strftime("%Y.%m.%d., %H:%M:%S")))
                    # terrarium_logger.info("TEMPERATURE: %s'c,\tHUMIDITY: %s\tDATE: %s ", temperature, humidity, time.strftime("%Y.%m.%d., %H:%M:%S"))
            with self._lock:
                try:
                    data2 = Sensor_2.read()
                except Exception as e:
                    # raise
                    pass
                else:
                    self.temperature2 = round(data2['temperature'], 3)
                    self.humidity2 = round(data2['humidity'], 3)
                    if self._temphumi2_callback is not None:
                        self._temphumi2_callback(self.temperature2, self.humidity2)
                    print("___DATA_2___\n\tTEMPERATURE: {}'C,\tHUMIDITY: {}%,\tDATE: {}.".format(data2['temperature'], data2['humidity'], time.strftime("%Y.%m.%d., %H:%M:%S")))
            LED.blink('GREEN_LED', 2) if data1['temperature'] > 18 and ((15 <= data1['humidity'] < 100) or (data1['humidity'] == 0)) else LED.blink('RED_LED', 4)
            time.sleep(self.DELAY)

    def _update_battery(self):
        while True:
            try:
                battery_p = self.read_battery_percentage()
                battery_v = self.read_battery_voltage()
            except Exception as e:
                raise
            else:
                if self._BATTERY_callback is not None:
                    self._BATTERY_callback(battery_p, battery_v)
                if 20 < battery_p < 50:
                    self._battery_warning(battery_p, battery_v)
                elif battery_p < 20:
                    self._low_battery(battery_p, battery_v)
                time.sleep(self.DELAY * 2)


    """SOCKET TRIGGERS"""
    def on_temp_humidity_change(self, callback):
        self._temphumi_callback = callback
    def on_temp_humidity2_change(self, callback):
        self._temphumi2_callback = callback
    def on_door_change(self, callback):
        self._door_callback = callback
    def on_LAMP_change(self, callback):
        self._LAMP_callback = callback
    def on_UVB_change(self, callback):
        self._UVB_callback = callback
    def on_HEATER_change(self, callback):
        self._HEATER_callback = callback
    def on_RAIN_change(self, callback):
        self._RAIN_callback = callback
    def on_BATTERY_change(self, callback):
        self._BATTERY_callback = callback


    """"REED RELAY"""
    def _door_change(self, pin):
        # Called by the RPI.GPIO library when the door pin changes state.
        # Check if someone has registered a thing door callback and call it with the current thing door state.
        if self._door_callback is not None:
            self._door_callback(REED_RELAY.state())
        # terrarium_logger.debug('DOOR state is %s', GPIO.input(int(configuration["REED_RELAY"]["REED_RELAY"])))

    def read_door(self):
        # Read the door state and return it's current value.
        with self._lock:
            return REED_RELAY.state()

    #
    # """"LAMP"""
    # def read_LAMP(self):
    #     # Read the LAMP state and return its current value.
    #     with self._lock:
    #         return LAMP.state()


    """LED"""
    def set_led(self, value):
        #Set the LED (On = True, Off = False)
        with self._lock:
            LED.switch_on('BLUE_LED') if value else LED.switch_off('BLUE_LED')


    """TEMPERATURE"""
    def check_temperature(self, temperature, humidity):
        if Scheduler.is_light_time():
            if (0 <= temperature <= 100) and (0 <= humidity <= 100): # Data validation
                if temperature <= (self.new_temperature_setpoint - self.temperature_threshold):
                    print('Heating ON.')
                    HEATER.switch_on()
                    self.HEATER_state = HEATER.ON
                    self._trigger_HEATER_callback()
                elif temperature >= (self.new_temperature_setpoint + self.temperature_threshold):
                    print('Heating OFF.')
                    HEATER.switch_off()
                    self.HEATER_state = HEATER.OFF
                    self._trigger_HEATER_callback()
                elif ((self.new_temperature_setpoint - self.temperature_threshold) < temperature < (self.new_temperature_setpoint + self.temperature_threshold)):
                    print('Temperature is in the range, no action was taken.')
            else:
                print('ERROR while checking the temperature.')
                HEATER.switch_off()
                self.HEATER_state = HEATER.OFF
                self._trigger_HEATER_callback()
                # terrarium_logger.error('ERROR with TEMPERATURE: %s', temperature)
        else:
            print('Not heating, out of timeframe or temp range.')
            HEATER.switch_off()
            self.HEATER_state = HEATER.OFF
            self._trigger_HEATER_callback()

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

        # Callback trigger on change
    def _trigger_HEATER_callback(self):
        if self._HEATER_callback is not None:
            self._HEATER_callback(self.HEATER_state)

    """RAIN"""

    # Callback trigger on change
    def _trigger_RAIN_callback(self):
        # Callback trigger on change
        if self._RAIN_callback is not None:
            self._RAIN_callback(self.RAIN_state)

    """"BATTERY"""
    def read_battery_percentage(self):
        # Read the battery percentage and return its current value.
        return round(BATTERY.read_percentage(), 3)

    def read_battery_voltage(self):
        # Read the battery percentage and return its current value.
        return round(BATTERY.read_voltage(), 3)

    def _battery_warning(self, battery_p, battery_v):
        print('[WARNING] Battery is below 50%.')
        self.battery_warning_count += 1
        if (self.battery_warning_count == 1) or (self.battery_warning_count % 5):
            IFTTT.send_webhooks_trigger('battery_low', battery_p, battery_v)

    def _low_battery(self, battery_p, battery_v):
        print('BATTERY LOW, SHUTTING DOWN...')
        IFTTT.send_webhooks_trigger('battery_low', battery_p, battery_v)
        exit_proc()
        os.system('sudo shutdown -h now')



if __name__ == "__main__":
    print('Press CTRL+C fo finish.')
    Flow()
    while True:
        pass
