#! /usr/bin/env python3

import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from terrarium import Pin_init as Pin_init
from terrarium import Configuration as Configuration
from terrarium import _dht_sensor


print('Starting {} test'.format(os.path.abspath(os.path.dirname(__file__))))

Pin_init = Pin_init.Pin_init(Configuration)
print('PINs are set.') if Pin_init.initialize_pins() else print('PIN ERROR')

try:
    dht1 = _dht_sensor.DHT_sensor(Configuration.DHT_SENSOR1)
except AttributeError as ae:
    print('ERROR: Sensor 1 is not set:\t{0}'.format(ae))
except Exception as e:
    raise
else:
    for n in range(3):
        th1 = dht1.read_dht()
        print('\ndata: {}\n'.format(th1))
        time.sleep(5)
finally:
    print('dht1 finally...')

try:
    dht2 = _dht_sensor.DHT_sensor(Configuration.DHT_SENSOR2)
except AttributeError as ae:
    print('ERROR: Sensor 2 is not set:\t{0}'.format(ae))
except Exception as e:
    raise
else:
    for n in range(3):
        th2 = dht1.read_dht()
        print('\ndata: {}\n'.format(th2))
        time.sleep(5)
finally:
    print('dht2 finally...')
