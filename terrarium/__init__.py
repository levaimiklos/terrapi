#! /usr/bin/env python3

import sys
from terrarium import configuration as Configuration
from terrarium import pin_init as Pin_init
from terrarium import scheduler as Scheduler
from terrarium import battery as Battery
from terrarium import controller as Controller

try:
    Pin_init = Pin_init.Pin_init(Configuration)
    Pin_init.initialize_pins()
except Exception as e:
    print('\n\nERROR:\n\t{}\n\nExiting...'.format(e))
    sys.exit(50)

Scheduler = Scheduler.Scheduler(Configuration.TIMING)
Battery = Battery.Battery()
