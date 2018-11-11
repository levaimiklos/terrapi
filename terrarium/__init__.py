#! /usr/bin/env python3

from terrarium import configuration as Configuration
from terrarium import pin_init as Pin_init
from terrarium import scheduler as Scheduler
from terrarium import battery as Battery
from terrarium import controller as Controller

try:
    Pin_init = Pin_init.Pin_init(Configuration)
except:
    raise
else:
    pin_init_success = Pin_init.initialize_pins()
    print('PINs are set.') if pin_init_success else print('PIN ERROR')

Scheduler = Scheduler.Scheduler(Configuration.TIMING)
Battery = Battery.Battery()
