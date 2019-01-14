#! /usr/bin/env python3

import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from terrarium import Configuration as Configuration
from terrarium import _bmx280_sensor as _bme280


print('Starting {} test'.format(os.path.abspath(os.path.dirname(__file__))))


try:
    bme = _bme280.sensor(Configuration.BMx_SENSOR)
except AttributeError as ae:
    print('ERROR: Sensor BME is not set:\t{0}'.format(ae))
except Exception as e:
    raise
else:
    for n in range(3):
        th1 = bme.read()
        print('\ndata: {}\n'.format(th1))
        time.sleep(10)
finally:
    print('bme finally...')
