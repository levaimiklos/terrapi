#! /usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))

from terrarium import configuration as Configuration
from terrarium import pin_init as Pin_init


Pin_init = Pin_init.Pin_init(Configuration)
print('PINs are set.') if Pin_init.initialize_pins() else print('PIN ERROR')
