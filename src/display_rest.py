#!/usr/bin/env python
# --------------------------------------------------
# IMPORT MODULES

from __future__ import division
import sys
import pygame
from pygame.locals import KEYDOWN
from display import DISPLAY
from datetime import datetime
import os
from poll import THREAD

#############################
# Import colors
import colors

#############################
# Import parameters
from parameters import FPS, fullscreen_on, param_rest, lj_trigger_emg


# Open the device file for the joystick.
joy_input = os.open(sys.argv[1], os.O_RDWR | os.O_NONBLOCK)

#
# Start THREAD
#
poll_thread = THREAD(None, None, joy_input)
poll_thread.daemon = True
poll_thread.start()


#
# Get param for the sequence
#
param = param_rest

#
# Start DISPLAY
#
mode = DISPLAY('USB connection', None, None, FPS, fullscreen_on)

running = True
#
# Fill screen in black - edged in white
#
mode.display.fill(colors.BLACK)
mode.display_edges()

#
# display all targets
#
mode.display_all_targets()
mode.update()

#
# Start Labjack
#
if param['start_emg']:
    import labjack_interface as lji
    lji.reset()

if param['mri_trigger']:
    pressFive = False
    while not poll_thread.joy_status['ttl'] and not pressFive:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                #
                # Quit if something goes wrong
                #
                if event.unicode == u'm':
                    pressFive = True

        mode.display_text('BE READY', colors.RED, 100)


while running:

    if mode.debug:
        print 'Start EMG'

    lji.run_stimulation(lj_trigger_emg)
    mode.display_text(' + ', colors.RED, 100, datetime.now(), param['rest_time'], False, False)
    running = False
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            #
            # Quit if something goes wrong
            #
            if event.unicode == u'q':
                running = False
                pygame.quit()
                sys.exit()
