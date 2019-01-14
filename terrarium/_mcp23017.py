#!/usr/bin/env python3

BUS = 1
MCP23017_DEVICE = 0x20
MCP23017_IODIRA = 0x00
MCP23017_OUTPUTS = 0x14
MCP23017_INPUTS = 0x12
MCP23017_DIROUT = 0x00 # == 0b00000000 # IODIRA 0==output 1==input
MCP23017_DIRIN = 0x11 # == 0b11111111 # IODIRA 0==output 1==input


class MCP23017_ctrl(object):

    def __init__(self):
        try:
            import smbus
        except Exception as e:
            # bus.write_byte_data(MCP23017_DEVICE, MCP23017_OUTPUTS, 0x00) # OLATA everything off
            raise
        else:
            self.bus = smbus.SMBus(BUS)
        try:
            self.bus.write_byte_data(MCP23017_DEVICE, MCP23017_IODIRA, MCP23017_DIROUT)
            # self.bus.write_byte_data(MCP23017_DEVICE, MCP23017_OUTPUTS, 0x00) # OLATA everything off
            self.bus.write_byte_data(MCP23017_DEVICE, MCP23017_OUTPUTS, 0xFF) # OLATA everything off
        except OSError as ose:
            print (ose)
            print('No MCP device is connected!\n\n')
        except:
            raise


    def on(self, PIN, VALUE):
        bit = PIN - 1
        current_value = self.bus.read_byte_data(MCP23017_DEVICE, MCP23017_INPUTS)
        print('register value: 0b{0:08b}'.format(current_value))
        if VALUE == 1:
            new_value = current_value | (1 << bit) # Set pin '1'
        elif VALUE == 0:
            new_value = current_value & (0xff - (1 << bit)) # Set pin '0'
        print('new value: 0b{0:08b}'.format(new_value))
        self.bus.write_byte_data(MCP23017_DEVICE, MCP23017_OUTPUTS, new_value)

    def off(self, PIN, VALUE):
        bit = PIN - 1
        current_value = self.bus.read_byte_data(MCP23017_DEVICE, MCP23017_INPUTS)
        print('register value: 0b{0:08b}'.format(current_value))
        if VALUE == 0:
            new_value = current_value & (0xff - (1 << bit)) # Set pin '0'
        elif VALUE == 1:
            new_value = current_value | (1 << bit) # Set pin '1'
        print('new value: 0b{0:08b}'.format(new_value))
        self.bus.write_byte_data(MCP23017_DEVICE, MCP23017_OUTPUTS, new_value)

    def all_low(self):
        self.bus.write_byte_data(MCP23017_DEVICE, MCP23017_OUTPUTS, 0x00) # OLATA everything off

    def all_high(self):
        self.bus.write_byte_data(MCP23017_DEVICE, MCP23017_OUTPUTS, 0xFF) # OLATA everything off

    def state(self):
        return self.bus.read_byte_data(MCP23017_DEVICE, MCP23017_INPUTS)
