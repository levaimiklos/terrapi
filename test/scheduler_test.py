#! /usr/bin/env python3

import os
import sys
import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from terrarium import Configuration as Configuration
from terrarium import Scheduler as Scheduler

print('---------------------')
lt = Scheduler.is_light_time()
print('LIGHT time.') if lt else print('NOT light time.')

print('---------------------')
uv = Scheduler.is_UVB_time()
print('UV time.') if uv else print('NOT UV time.')

print('---------------------')
