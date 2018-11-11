#! /usr/bin/env python3

import time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
#
# from terrarium import Configuration
# from terrarium import Scheduler
# from terrarium import Controller
#
#
# SLEEP = 5
#
# scheduler = Scheduler.Scheduler(Configuration.TIMING)
# lamp = Controller.Lamp(Configuration.TOOLS)
#
# try:
#  while True:
#   if scheduler.is_light_time():
#    print('It is light time.')
#    lamp.switch_on()
#   else:
#    print('Not light time.')
#    lamp.switch_off()
#   print('lamp state: {0}'.format(lamp.state()))
#   time.sleep(SLEEP)
#
# except:
#  raise
#  print('END')

import terrarium
from terrarium import Scheduler as Scheduler
from terrarium import configuration as Configuration


Scheduler = Scheduler.Scheduler(Configuration.TIMING)
lt = Scheduler.is_light_time()
print('LIGHT time.') if lt else print('NOT light time.')
