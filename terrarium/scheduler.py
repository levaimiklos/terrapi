#! /usr/bin/env python3

import datetime

class Scheduler(object):

    def __init__(self, Configuration):
        self.uvb_delay = datetime.timedelta(minutes = Configuration['uvb_delay'])
        self.start_time = datetime.time(hour = Configuration['start_light_time_hour'], minute = Configuration['start_light_time_minute'], second = 0)
        self.stop_time = datetime.time(hour = Configuration['stop_light_time_hour'], minute = Configuration['stop_light_time_minute'], second = 0)
        # print('start time: {0}\tstop time: {1}'.format(self.start_light_time, self.stop_light_time))

    def _convert(self, init_time):
        try:
            if type(init_time) is datetime.time:
                pass
            elif type(init_time) is datetime.datetime:
                pass
            else:
                raise AttributeError
        except AttributeError:
            print('[ERROR] Scheduler: Must pass a datetime or time object.')
            return 'attribution error'
        except Exception as e:
            raise
        else:
            return datetime.datetime.now().replace(hour = init_time.hour, minute = init_time.minute, second = init_time.second)

    def _values(self):
        self.current_time = datetime.datetime.now()
        # print('current: ', self.current_time, type(self.current_time))
        self.start_light_time = self._convert(self.start_time)
        # print('start: ', self.start_light_time, type(self.start_light_time))
        self.stop_light_time = self._convert(self.stop_time)
        # print('stop: ', self.stop_light_time, type(self.stop_light_time))
        self.start_uvb_time = self.start_light_time - self.uvb_delay
        # print('start uv: ', self.start_uvb_time, type(self.start_uvb_time))
        self.stop_uvb_time = self.stop_light_time + self.uvb_delay
        # print('stop uv: ', self.stop_uvb_time, type(self.stop_uvb_time))


    def is_light_time(self):
        self._values()
        try:
            if self.start_light_time > self.stop_light_time:
                raise ValueError
            elif self.start_light_time < self.current_time < self.stop_light_time:
                return True
            else:
                return False
        except ValueError as ve:
            print(ve, '\n[ERROR] Scheduler: Stop time should be later than start time.\n')
            return False
        except Exception as e:
            print(e)
            return False

    def is_UVB_time(self):
        self._values()
        try:
            if self.start_light_time > self.stop_light_time:
                raise ValueError
            elif self.start_uvb_time < self.current_time < self.stop_uvb_time:
                return True
            else:
                return False
        except ValueError as ve:
            print(ve, '\n[ERROR] Scheduler: Stop time should be later than start time.\n')
            return False
        except Exception as e:
            print(e)
            return False
