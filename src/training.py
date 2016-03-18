#!/usr/bin/env python
# --------------------------------------------------
# IMPORT MODULES

from __future__ import division

import sys
import os
import pygame
from pygame.locals import QUIT, KEYDOWN
from datetime import timedelta
from datetime import datetime

from display import DISPLAY
from poll import THREAD

#############################
# Import colors
import colors

#############################
# Import parameters
from parameters import *

param = param_training
#############################
# Import target creation function
from utils import create_targets_list, get_logfile, log, log_header, load_calibration, extract_min_rt

##############################
# TODO MODIFICATION OF THE INPUT
# Open the device file for the joystick.
joy_input = os.open(sys.argv[1], os.O_RDWR | os.O_NONBLOCK)

#
# Input subject id
#
print "Enter the ID: "
subject_id = raw_input()
logfilename = get_logfile(subject_id,'training')

#
# get joystick range
#
joy_range = load_calibration()

#
# Start THREAD
#
poll_thread = THREAD(joy_range, logfilename, joy_input)
poll_thread.daemon = True
poll_thread.start()

#
# Start DISPLAY
#
mode = DISPLAY('USB connection', poll_thread, task_info, FPS, fullscreen_on)

#
# write header
#
log_header(poll_thread.logfile, poll_thread.joy_status, mode.task_info, joy_range)

#
# Start Labjack
#
if param['start_emg'] or param['run_stimulation'] or param['monitor_emg']:
    import labjack_interface as lji
    lji.reset()
    mode.task_info['description'] = 'start labjack'
    mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
    log(poll_thread.logfile, poll_thread. joy_status, mode.task_info)


target_on = False

#
# 6 : PSEUDO RANDOM
#
list_seq_targets = create_targets_list(param, 6)

##############################

target_still = False

running = True

#
# wait for mri then log
#
if param['mri_trigger']:
    while not poll_thread.joy_status['ttl']:

        if debug_mode:
            print(poll_thread.joy_status['ttl'])

        mode.display_text('BE READY', colors.RED, 100)

    mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
    mode.task_info['description'] = 'start mri'
    log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)
    poll_thread.joy_status['ttl'] = False

    if param['start_emg']:
        lji.run_stimulation(lj_trigger_emg)
        mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
        mode.task_info['description'] = 'start EMG'
        log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

elif param['start_emg']:
    lji.run_stimulation(lj_trigger_emg)
    mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
    mode.task_info['description'] = 'start EMG'
    log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)




#
# draw a red cross
#
mode.display_text('+', colors.RED, 100, datetime.now(), param['rest_time'])
#
# log first bloc
#
mode.task_info['description'] = 'start bloc'
mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)
mode.log_start_bloc = False


start_target_found = False
validation_target = False

while running and mode.task_info['numBloc'] < param['nbBlocs']:

    if mode.task_info['numBloc'] >= 1 and mode.task_info['numTarget'] == 0 and mode.log_start_bloc:

        #
        #   log beginning of a bloc
        #
        mode.task_info['description'] = 'start bloc'
        mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
        log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)
        mode.log_start_bloc = False

    #
    # Get position of the target
    #
    mode.task_info['position_target'] = int(list_seq_targets[mode.task_info['numTarget']])

    #
    # Fill screen in black - edged in white
    #
    mode.display.fill(colors.BLACK)
    mode.display_edges()

    #
    # display all targets
    #
    mode.display_all_targets()

    #
    # display one target
    #
    mode.display_target(True)

    #
    # display cursor
    #
    mode.display_cursor()

    #
    # if target reached
    #
    if mode.target_found(start_target_found) and not start_target_found and not validation_target:
        start_time_target_found = datetime.now()
        start_target_found = True

    #
    # participant needs to stay still for param['time_target'] seconds
    #
    if start_target_found:
        if datetime.now() >= (start_time_target_found + timedelta(seconds=float(param['time_target']))) and mode.target_found(start_target_found):
            #
            # target validated
            #
            start_target_found = False
            validation_target = True

            mode.task_info['description'] = 'Target end'
            mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
            log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

        elif datetime.now() >= start_time_target_found + timedelta(seconds=float(param['time_target'])) and not mode.target_found(start_target_found):
            #
            # target not validated
            #
            mode.task_info['description'] = 'Target not reached'
            mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
            log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

            validation_target = False
            start_target_found = False

    if validation_target:

        validation_target = False
        mode.need_display_target = True

        #
        # next target
        #
        mode.task_info['numTarget'] += 1

        if mode.task_info['numTarget'] >= param['nbKeys']:

            #
            #   log end of a bloc
            #
            mode.task_info['description'] = 'end bloc'
            mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
            log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

            ####################
            # New Random targets
            ####################
            # 1 : RANDOM
            # 6 : PSEUDO RANDOM
            list_seq_targets = create_targets_list(param, 6)

            #
            # fill screen in black
            #
            mode.display.fill(colors.BLACK)

            #
            # update values
            #
            mode.task_info['numTarget'] = 0
            mode.task_info['numBloc'] += 1
            mode.log_start_bloc = True

            #
            # rest period
            #
            mode.display_text('+', colors.RED, 100, datetime.now(), param['rest_time'])

    #
    # update screen
    #
    mode.update()

    for event in pygame.event.get():
        print event.type
        if event.type == QUIT:
            if mri_training:
                lji.reset()
                mode.task_info['description'] = 'stop labjack'
                mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
                log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

            running = False
            poll_thread.logfile.close()
            quit()
            poll_thread.stop()
            sys.exit()
        if event.type == KEYDOWN:
            #
            # Quit if something goes wrong
            #
            if event.unicode == u'q':
                running = False
                poll_thread.logfile.close()
                pygame.quit()
                poll_thread.stop()
                sys.exit()

#
# close log file
#
poll_thread.logfile.close()

#
# close pygame and thread
#
poll_thread.stop()

#
# extraction of meanRT
#
print 'Start extraction'
extract_min_rt(subject_id, logfilename, param)
print 'End extraction'

quit()
sys.exit()
