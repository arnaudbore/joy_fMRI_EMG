__author__ = 'labdoyon'
from collections import deque
import numpy as np
import labjack_interface as lji


class AnalogPlot:
    def __init__(self, io_lj, maxBuff, debug):
        self.buff = deque([0.0] * maxBuff)
        self.maxBuff = maxBuff
        self.max = 1
        self.min = 1e8
        self.io = io_lj
        self.debug = debug

    # add to buffer
    def addToBuf(self, val):
        if len(self.buff) < self.maxBuff:
            self.buff.append(val)
        else:
            self.buff.pop()
            self.buff.appendleft(val)

    # update max value
    def update(self, min_max=False):
        inData = lji.read_analog(self.io)
        self.addToBuf(inData)
        if not self.buff.count(0) and min_max:
            val_temp = np.trapz(np.abs(self.buff))
            if self.max < val_temp:
                self.max = val_temp
            if self.min > val_temp:
                self.min = val_temp

            del val_temp

    def print_parameters(self):
        print('Max: ',self.max)
        print('Min: ',self.min)

    def readCurrentValue(self):
        print(lji.read_analog(self.io))