TIMING = {
    'start_light_time_hour' : 8,
    'start_light_time_minute' : 0,
    'stop_light_time_hour' : 20,
    'stop_light_time_minute' : 0,
    'delay' : 30, #sec
    'uvb_delay' : 30, #min
    'rain_1' : 8,
    'rain_2' : 18
    }

CONTROLLER = {
    'set_temperature' : 20,
    'temperature_threshold' : 2,
    }

REED_RELAY = {
    # sensor_type : pin
    'REED_RELAY' : 12
    }

LEDS = {
    # color  : pin
    'RED_LED' : 13,
    'GREEN_LED' : 22,
    'BLUE_LED' : 27
    }

TOOLS = {
    # type      : pin
   'LAMP' : 1,
   'UVB' : 2,
   'HEATER' : 3,
   'RAIN' : 4
   }

DHT_SENSOR1 = {
    'DHT_TYPE' : 11,
    'DHT_PIN' : 5,
#    'DHT_RESET_PIN' : 21,
#    'DHT_ERROR_THRESHOLD' : 2
    }

DHT_SENSOR2 = {
    'DHT_TYPE' : 11,
    'DHT_PIN' : 6,
#    'DHT_RESET_PIN' : 21,
#    'DHT_ERROR_THRESHOLD' : 2
    }

BMx_SENSOR = {
    'TYPE' : 'BMP280'
    }
