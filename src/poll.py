__author__ = 'abore'

import struct
import os
import threading
import time

# This is the event system's format.
joy_format = "LLHHi"

# JOYSTICK INFORMATION
joy_status = {'button1': 0,
              'button3': 0,
              'ttl': False,
              'x_sensor': 512,
              'y_sensor': 512,
              'x_monitor': 0.5,
              'y_monitor': 0.5}


class THREAD(threading.Thread):

    def __init__(self,joy_range=None, logfilename=None, joy_input=None):
        threading.Thread.__init__(self)
        self.Terminated = False
        self.joy_status = joy_status
        self.joy_range = joy_range
        if logfilename is not None:
            self.logfile = open(logfilename, 'w')
        if joy_input is None:
            self.joy_input = []
        else:
            self.joy_input = joy_input

    def run(self):
        while not self.Terminated:

            jv = self.poll()
            if jv is None:
                time.sleep(.001)
            else:
                joy_info = struct.unpack(joy_format, jv)
                secs = joy_info[0]
                usecs = joy_info[1]
                packed_type = joy_info[2]
                packed_code = joy_info[3]
                packed_value = joy_info[4]

                if packed_type == 0x03:

                    if packed_code == 0x00:
                        joy_status['x_sensor'] = packed_value
                    if packed_code == 0x01:
                        joy_status['y_sensor'] = packed_value

                if packed_type == 0x01:
                    if packed_code == 288:
                        joy_status['button1'] = packed_value
                    if packed_code == 290:
                        joy_status['button3'] = packed_value
                    if packed_code == 289:
                        joy_status['ttl'] = True

    def stop(self):
        self.Terminated = True


    def poll(self):
        try:
            joy_buffer = os.read(self.joy_input, struct.calcsize(joy_format))
            return joy_buffer
        except OSError:
            return None