#! /usr/bin/env python3

# import os
# import time
# import RPi.GPIO as GPIO
# import Adafruit_DHT as DHT
#
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
try:
    from terrarium import Configuration as cfg
    print('Configuration imported')
except:
    raise

print(cfg.DHT_SENSOR1)
a = cfg.DHT_SENSOR1.get('DHT_RESET_PIN', 'Fail')
print(a)
