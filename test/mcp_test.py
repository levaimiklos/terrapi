#!/usr/bin/env python3

import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

try:
    from terrarium import _mcp23017 as MCP
except:
    raise

DELAY = 0.2

ctrl = MCP.MCP23017_ctrl()

try:
    ctrl.on(1, 1)
    time.sleep(DELAY)

    ctrl.on(3, 1)
    time.sleep(DELAY)

    ctrl.off(3, 0)
    time.sleep(DELAY)

    ctrl.off(1, 0)
    time.sleep(DELAY)

    ctrl.on(2, 0)
    time.sleep(DELAY)

    ctrl.off(2, 1)
    time.sleep(DELAY)

    ctrl.on(4, 0)
    time.sleep(DELAY)

    ctrl.off(4, 1)
    time.sleep(DELAY)

except Exception as e:
    raise

finally:
    ctrl.all_high()
    time.sleep(DELAY)
    ctrl.all_low()
    time.sleep(DELAY)
    ctrl.all_high()
