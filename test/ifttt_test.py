#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from terrarium import IFTTT as IFTTT

print("IFTTT key is: {}".format(IFTTT.webhooks_key))
print("IFTTT key type: {}".format(type(IFTTT.webhooks_key)))

t = IFTTT.send_webhooks_trigger("battery_low", 21, 11)
