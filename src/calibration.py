#!/usr/bin/env python
# --------------------------------------------------
# IMPORT MODULES

from __future__ import division

import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN
from datetime import datetime

# Import current directory
sys.path.append(os.getcwd())
cwd = os.getcwd()

#############################
# Import colors
import colors

#############################
# Import parameters
from parameters import *

from display import DISPLAY
from poll import THREAD

from utils import update_range, update_center, get_logfile, log_header, save_calibration

# Open the device file for the joystick.
joy_input = os.open(sys.argv[1], os.O_RDWR | os.O_NONBLOCK)

#
# Input subject id
#
print "Enter the ID: "
subject_id = raw_input()
logfilename = get_logfile(subject_id,'calibration')

#
# start THREAD
#
poll_thread = THREAD(joy_range, logfilename, joy_input)
poll_thread.daemon = True
poll_thread.start()

#
# start DISPLAY
#
mode = DISPLAY('USB connection', poll_thread, task_info, FPS, fullscreen_on)

#
# write header
#
log_header(poll_thread.logfile, poll_thread.joy_status, mode.task_info)


#
# display calibration
#
mode.display.fill(colors.BLACK)
mode.display_text('CALIBRATION', colors.RED, 100, datetime.now(), 5)
mode.display_text(calibration_string[0], colors.RED, 50, datetime.now(), 2)

running_calibration = True
next_order = True

calibration_string_order = 0

while running_calibration:
    # Fill screen in black
    mode.display.fill(colors.BLACK)
    mode.display_edges()

    if next_order:
    #
    # display order
    #
        mode.display_text(calibration_string[calibration_string_order], colors.RED, 50, datetime.now(), 2)
        next_order = False


    if debug_mode:
        print 'jx-jy: ' + str(poll_thread.joy_status['x_sensor']) + '-' + str(poll_thread.joy_status['y_sensor'])

    mode.display_cursor()

    if calibration_string_order == 0:
        poll_thread.joy_range = update_center(poll_thread.joy_status, poll_thread.joy_range)
    else:
        poll_thread.joy_range = update_range(poll_thread.joy_status, poll_thread.joy_range)

    ################
    # UPDATE SCREEN
    mode.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running_calibration = False
        if event.type == KEYDOWN:
            ################
            # Quit if something goes wrong
            if event.unicode == u'q':
                running_calibration = False
            if event.unicode == u'n':
                calibration_string_order += 1
                next_order = True
            if event.unicode == u'n' and calibration_string_order>4:
                running_calibration = False


print(joy_range)
save_calibration(subject_id, poll_thread.joy_range)

# CALIBRATION
###################################################
###################################################