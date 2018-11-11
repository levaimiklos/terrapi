#! /usr/bin/env python3

import datetime

class Scheduler(object):

    def __init__(self, Configuration):
        start_light_time_hour = Configuration['start_light_time_hour']
        start_light_time_minute = Configuration['start_light_time_minute']
        stop_light_time_hour = Configuration['stop_light_time_hour']
        stop_light_time_minute = Configuration['stop_light_time_minute']
        self.start_light_time = datetime.time(hour = start_light_time_hour, minute = start_light_time_minute, second = 0)
        self.stop_light_time = datetime.time(hour = stop_light_time_hour, minute = stop_light_time_minute, second = 0)
        # print('start time: {0}\tstop time: {1}'.format(self.start_light_time, self.stop_light_time))

    def is_light_time(self):
        current_time = datetime.time(hour=datetime.datetime.now().hour, minute=datetime.datetime.now().minute, second=datetime.datetime.now().second)
        # print('current time: {0}'.format(current_time))
        if self.start_light_time > self.stop_light_time:
            # print('ERROR: stop time should be later than start time.')
            return False
        elif self.start_light_time < current_time < self.stop_light_time:
            return True
        else:
            return False
