#! /usr/bin/env python3

def _operation(operation, value):
    if operation == 'trimToTwo':
        return (value & 0xFFFF)
    elif operation == 'toLittleEndian':
        return (((value & 0xFF) << 8) | (value >> 8))
