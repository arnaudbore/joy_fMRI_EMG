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

#
# Import colors
#
import colors

#
# Import parameters
#
from parameters import *

#
# Get param for the sequence
#
param = param_task

#
# Import target creation function
#
from utils import (create_targets_list,
                   get_logfile,
                   log,
                   log_header,
                   load_calibration,
                   get_min_rt_from_rtfile,
                   extract_RT_feedback)

##############################
# TODO MODIFICATION OF THE INPUT
# Open the device file for the joystick.
joy_input = os.open(sys.argv[1], os.O_RDWR | os.O_NONBLOCK)


#
# Input subject id
#
print "Enter the ID: "
subject_id = raw_input()


mode_sequence = False
mode_ctrl = False

if float(sys.argv[2]) == 1:
    logfilename = get_logfile(subject_id,'msl')
    mode_sequence = True
elif float(sys.argv[2]) == 2:
    logfilename = get_logfile(subject_id,'rnd')
else:
    logfilename = get_logfile(subject_id,'ctrl')
    mode_ctrl = True

#
# RT FROM TRAINING
#
min_median_ref = get_min_rt_from_rtfile(subject_id)

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

##############################
# Start DISPLAY
mode = DISPLAY('USB connection', poll_thread, task_info, FPS, fullscreen_on, debug_mode)

mode.task_info['subject_id'] = subject_id

#
# write header
#
log_header(poll_thread.logfile, poll_thread.joy_status, mode.task_info, poll_thread.joy_range, min_median_ref)

#
# Start Labjack
#
if param['start_emg'] or param['run_stimulation'] or param['monitor_emg']:
    import labjack_interface as lji
    lji.reset()
    mode.task_info['description'] = 'start labjack'
    mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
    log(poll_thread.logfile, poll_thread. joy_status,mode.task_info)

target_on = False

#
# CREATION TARGETS:
# 2 = SEQUENCE
# 4 = CTRL
# 3 = RND
#
if mode_sequence:
    list_seq_targets = create_targets_list(param, 2)
elif mode_ctrl:
    list_seq_targets = create_targets_list(param, 4)
else:  # 6 for pseudo-random and 1 for real random with the same num of targets
    list_seq_targets = create_targets_list(param, 6)

target_still = False
running = True

#
# wait for mri then log
#
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

    mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
    mode.task_info['description'] = 'start mri'
    log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)
    poll_thread.joy_status['ttl'] = False

if param['start_emg']:
    if mode.debug:
        print 'Start EMG'

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

            mode.task_info['description'] = 'target end'
            mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")

            #
            # mode.targets_start_end to compute feedback information
            #
            mode.targets_start_end.append(datetime.now())
            log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

        elif datetime.now() >= start_time_target_found + timedelta(seconds=float(param['time_target'])) and not mode.target_found(start_target_found):
            #
            # target not validated
            #
            mode.task_info['description'] = 'target not reached'
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

            #
            # CREATION TARGETS:
            # 2 = SEQUENCE
            # 4 = CTRL
            # 6 = RND
            #
            if mode_sequence:
                list_seq_targets = create_targets_list(param, 2)
            elif mode_ctrl:
                list_seq_targets = create_targets_list(param, 4)
            else:
                old_list_targets = list_seq_targets
                while old_list_targets == list_seq_targets:
                    list_seq_targets = create_targets_list(param, 6)

            if param['feedback']:
                #
                # fill screen in black
                #
                mode.display.fill(colors.BLACK)

                #
                # compute number of targets where rt is faster
                #
                [mode.targets_start_end, min_median_ref, value_inf_median] = extract_RT_feedback(mode.targets_start_end,
                                                                                             min_median_ref,
                                                                                             param)

                #
                # Feedback about speed of execution during the task
                #
                if language:
                    message = 'Vous avez ete ' + str("{:.2f}".format(len(value_inf_median) * 100 / (
                        param['nbKeys'] - 1))) + '% plus rapide !'
                else:
                    message = 'You had been ' + str("{:.2f}".format(len(value_inf_median) * 100 / (
                        param['nbKeys'] - 1))) + '% faster !'

                mode.display_text(message, colors.RED, 45, datetime.now(), 3)

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
            # New bloc of rest
            #
            mode.task_info['numBloc_rest'] += 1

            #
            # if stimulation
            #
            if mode.debug:
                print '###################################################################################'
                print 'Number of the rest bloc: ' + str(mode.task_info['numBloc_rest'])
                print 'Bloc where we want stimulation: ' + str(param['numBloc_Reststim'])

            if param['run_stimulation'] and mode.task_info['numBloc_rest'] in param['numBloc_Reststim']:

                start_stimulation = datetime.now()

                #
                # run stimulation
                #
                lji.run_stimulation(lj_trigger_stim)

                #
                # log information
                #
                mode.task_info['description'] = 'trigger stimulation'
                mode.task_info['time'] = start_stimulation.strftime("%H:%M:%S.%f")
                log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

                #
                # rest period
                #
                if mode.debug:
                    print '######################################################################################'
                    print 'REST PERIOD'

                mode.display_rest('+ s', colors.RED, 100, start_stimulation, param, True)
                # mode.display_text('+', colors.RED, 100, start_stimulation, param['rest_time'])

            else:
                #
                # rest period
                #
                mode.display_text('+', colors.RED, 100, datetime.now(), param['rest_time'])

    #
    # update screen
    #
    mode.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            if param['start_emg'] or param['run_stimulation'] or param['monitor_emg']:
                lji.reset()
                mode.task_info['description'] = 'stop labjack'
                mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
                log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)


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
                if param['start_emg'] or param['run_stimulation'] or param['monitor_emg']:
                    lji.reset()
                    mode.task_info['description'] = 'stop labjack'
                    mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
                    log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

                poll_thread.logfile.close()
                pygame.quit()
                poll_thread.stop()
                sys.exit()

#
# reset labjack
#
if param['start_emg'] or param['run_stimulation'] or param['monitor_emg']:
    lji.reset()
    mode.task_info['description'] = 'stop labjack'
    mode.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
    log(poll_thread.logfile, poll_thread.joy_status, mode.task_info)

#
# close log file
#
poll_thread.logfile.close()

#
# close pygame and thread
#
poll_thread.stop()
quit()

sys.exit()
