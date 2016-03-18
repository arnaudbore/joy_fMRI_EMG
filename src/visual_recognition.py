#!/usr/bin/env python
# --------------------------------------------------
# IMPORT MODULES

from __future__ import division

import sys
import pygame
from pygame.locals import QUIT, KEYDOWN

from display import DISPLAY

#
# Import colors
#
import colors

#
# Import parameters
#
from parameters import FPS, fullscreen_on, param_task, task_info, list_seq_recognition

#
# Get param for the sequence
#
param = param_task

#
# Import target creation function
#
from utils import create_targets_list


mode_sequence = True
list_seq_targets = create_targets_list(param, 2)

#
# Start DISPLAY
#

mode = DISPLAY(None, None, task_info, FPS, fullscreen_on)

position_target = 0

# Training == target random
list_seq_targets = create_targets_list(param_task, 2)

print list_seq_targets

running = True
keep_learning = True


mode.task_info['numTarget'] = 0


while running:
    if keep_learning:
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
        mode.display_target(False)
        mode.need_display_target = False

        if mode.task_info['numTarget'] > len(param_task['seqUsed'])-1:
            keep_learning = mode.display_text('Continue (y/n) ?', colors.RED, 45, None, 3600, True)
            mode.task_info['numTarget'] = 0
    else:
        num_list = 0
        for recognition in list_seq_recognition:
            answer = 'r'
            while answer == 'r':
                #
                # Example of sequence
                #
                mode.display_sequence(recognition,len(param_task['seqUsed']))

                #
                # Good or Bad sequence or Repeat the sequence
                #
                answer = mode.display_text('Good sequence or not  (y/n or repeat - r)', colors.RED, 45, None, 3600, True)

                if answer == 'r':
                    print 'Repeat'
                elif answer and (num_list == 2 or num_list == 4):
                        print 'Correct'
                elif not answer and (num_list == 0 or num_list == 1 or num_list == 3 or num_list == 5):
                    print 'Correct'
                else:
                    print 'Not Correct'
                    running = False
                    pygame.quit()
                    sys.exit()

            if num_list == 5:
                running = False
                pygame.quit()
                sys.exit()

            num_list += 1

    ################
    # UPDATE SCREEN
    mode.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            ################
            # Quit if something goes wrong
            if event.unicode == u'q':
                running = False
                pygame.quit()
                sys.exit()

            if (event.unicode == u'c') and keep_learning:
                mode.task_info['numTarget'] += 1
                mode.need_display_target = True
            # if (event.unicode == u'1') and not keep_learning:
            #    NUM_TARGET = NUM_TARGET+1


pygame.quit()
sys.exit()
