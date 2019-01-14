#!/usr/bin/env python3

import Adafruit_BME280 as BMx280

class sensor(object):

    def __init__(self, configuration):
        sensor_type = configuration['TYPE']
        self.temperature = None
        self.humidity = None
        if sensor_type in ['BMP280', 'BMP_280', 'bmp280', 'bmp_280']:
            self.sensor = BMx280.BME280(t_mode=BMx280.BME280_OSAMPLE_8, p_mode=BMx280.BME280_OSAMPLE_8, h_mode=BMx280.BME280_OSAMPLE_8)
            self.humidity = 0
        elif sensor_type in ['BME280', 'BME_280', 'bme280', 'bme_280']:
            self.sensor = BMx280.BME280(t_mode=BMx280.BME280_OSAMPLE_8, p_mode=BMx280.BME280_OSAMPLE_8, h_mode=BMx280.BME280_OSAMPLE_8)
            self.humidity = 1

    def read(self):
        try:
            self.temperature = self.sensor.read_temperature()
            if self.humidity:
                self.humidity = self.sensor.read_humidity()
        except Exception as e:
            raise
        finally:
            return {'temperature' : self.temperature,
                    'humidity' : self.humidity}
