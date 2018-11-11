#! /usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from terrarium import Configuration as Configuration
from terrarium import Scheduler as Scheduler


Scheduler = Scheduler.Scheduler(Configuration.TIMING)
lt = Scheduler.is_light_time()
print('LIGHT time.') if lt else print('NOT light time.')
