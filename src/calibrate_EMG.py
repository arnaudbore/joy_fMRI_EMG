#!/usr/bin/env python
# --------------------------------------------------
# IMPORT MODULES

from __future__ import division

import sys
import pygame
from pygame.locals import KEYDOWN
from display import DISPLAY
import lji_realtime as lji_rt
from utils import get_logfile, save_emg_calibration, load_emg_calibration
#############################
# Import colors
import colors

#############################
# Import parameters
from parameters import FPS, fullscreen_on, lj_monitor_emg, emg_buffer, debug_mode

#
# Input subject id
#
print "Enter the ID: "
subject_id = raw_input()
logfilename = get_logfile(subject_id,'calibration')

#
# Start DISPLAY
#
mode = DISPLAY('USB connection', None, None, FPS, fullscreen_on, debug_mode)

running = True
#
# Fill screen in black - edged in white
#
mode.display.fill(colors.BLACK)
mode.display_edges()

#
# display all targets
#
rt_plot = lji_rt.AnalogPlot(lj_monitor_emg, emg_buffer, debug_mode)

# Calibration get_minmax
get_minmax = True

if float(sys.argv[1]) == 0:
    # load calibration emg
    get_minmax = False
    [rt_plot.min, rt_plot.max] = load_emg_calibration(subject_id)

while running:
    mode.display_monitor_emg(rt_plot, get_minmax)

    mode.update()
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            #
            # Quit if something goes wrong
            #
            if event.unicode == u'q':
                if get_minmax: # If calibration
                    #################################
                    #Create calibration file for EMG
                    print('Maximum value : ' + str(rt_plot.max))
                    print('Minimal value : ' + str(rt_plot.min))

                    save_emg_calibration(rt_plot, subject_id)

                running = False
                pygame.quit()
                sys.exit()

