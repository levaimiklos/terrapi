#! /usr/bin/env python3

import sys
from terrarium import configuration as Configuration
from terrarium import pin_init as Pin_init
from terrarium import scheduler as Scheduler
from terrarium import battery as Battery
from terrarium import controller as Controller
from terrarium import ifttt as IFTTT


try:
    Pin_init = Pin_init.Pin_init(Configuration)
    Pin_init.initialize_pins()
except Exception as e:
    print('\n\nERROR:\n\t{}\n\nExiting...'.format(e))
    sys.exit(50)


Scheduler = Scheduler.Scheduler(Configuration.TIMING)
# Battery = Battery.Battery()


webhooks = "/home/pi/webhooks.txt"
try:
    with open (webhooks, 'r') as webhooks:
        try:
            infile_content = webhooks.readlines()
            webhooks_key = infile_content[0].split('\n')[0]
        except:
            raise
except IOError:
    print('Unable to open {}'.format(webhooks))
except:
    raise
else:
    IFTTT = IFTTT.IFTTT(webhooks_key)
