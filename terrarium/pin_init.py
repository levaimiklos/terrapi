#! /usr/bin/env python3

import time
import RPi.GPIO as GPIO

class Pin_init(object):

    def __init__(self, Configuration):
        self.configuration = Configuration
        self.pin_init_success = None

    def initialize_pins(self):
        try:
            print('Initializing PINs.')
            """Initialize PINs"""
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
#            all = [14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26]
#            for p in all:
#                GPIO.setup(p, GPIO.OUT, initial = GPIO.LOW)

            """LEDS"""
            for pin in self.configuration.LEDS:
                GPIO.setup(self.configuration.LEDS[pin], GPIO.OUT, initial = GPIO.LOW)

            # """TOOLS"""
            # for pin in self.configuration.TOOLS:
            #     GPIO.setup(self.configuration.TOOLS[pin], GPIO.OUT, initial = GPIO.HIGH)

            """REED_RELAY"""
            for pin in self.configuration.REED_RELAY:
                GPIO.setup(self.configuration.REED_RELAY[pin], GPIO.IN, pull_up_down=GPIO.PUD_UP)

            """DHT_SENSOR(S)"""
            # Sensor 1
            try:
                if self.configuration.DHT_SENSOR1:
                    pass
            except AttributeError as ae:
                pass
            except Exception as e:
                raise
            else:
                GPIO.setup(self.configuration.DHT_SENSOR1['DHT_PIN'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
                # GPIO.setup(self.configuration.DHT_SENSOR1['DHT_RESET_PIN'], GPIO.OUT, initial = GPIO.HIGH)
            # Sensor 2
            try:
                if self.configuration.DHT_SENSOR2:
                    pass
            except AttributeError as ae:
                pass
            except Exception as e:
                raise
            else:
                GPIO.setup(self.configuration.DHT_SENSOR2['DHT_PIN'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
                # GPIO.setup(self.configuration.DHT_SENSOR2['DHT_RESET_PIN'], GPIO.OUT, initial = GPIO.HIGH)

            self.pin_init_success = True

            # """BLINK 3 after setup done."""
            # for i in range(3):
            #     GPIO.output(self.configuration.LEDS["GREEN_LED"], 1)
            #     time.sleep(0.2)
            #     GPIO.output(self.configuration.LEDS["GREEN_LED"], 0)
            #     time.sleep(0.2)

            print('Initialization finished successfully.')

        except:
            self.pin_init_success = False
            # """BLINK 3 after setup done."""
            # for i in range(3):
            #     GPIO.output(self.configuration.LEDS["RED_LED"], 1)
            #     time.sleep(0.2)
            #     GPIO.output(self.configuration.LEDS["RED_LED"], 0)
            #     time.sleep(0.2)
            print('Initialization failed.')
            raise

        # TRUE if all PINs are set, else FALSE
        return self.pin_init_success
