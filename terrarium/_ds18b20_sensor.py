#!/usr/bin/env python3

import os


class sensor(object):

    def __init__(self):
        pass

    def read(self):
        # print('Reading DS18B20 sensor...')
        DIR = "/sys/bus/w1/devices/"
        DEVICES=[]
        item_num=1
        try:
            for FOLDERS in os.listdir(DIR):
                if FOLDERS.startswith("28"):
                    # print ("DS18B20 device %s : %s"%(item_num,FOLDERS))
                    DEVICES.append(FOLDERS)
                    item_num += 1
            if len(DEVICES) != 0:
                for d in range(len(DEVICES)):
                    t_file = DIR + DEVICES[d] + "/w1_slave"
                    # print("path: ", t_file)
                    try:
                        with open (t_file, 'r') as t_in:
                            try:
                                infile_content = t_in.readlines()
                                # print("infile_content: ", infile_content)
                                if str(infile_content[0].split(' ')[0]) != "00":
                                    temperature = float(infile_content[1].split(' ')[9][2:]) / 1000
                                    # print("sensor: {}\ttemperature: {}'C\thumidity: NA\tDate: {}".format(DEVICES[d], temperature, time.strftime("%Y-%m-%d_%H:%M:%S")))
                                else:
                                    print("CRC error, no temp data available...")
                            except:
                                raise
                    except IOError:
                        print('Unable to open {}'.format(t_file))
            else:
                print('No DS18B20 device was found.')
        except:
            raise

        finally:
            return { 'temperature' : temperature if temperature else -1,
                     'humidity' : 0 }
