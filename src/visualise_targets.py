#!/usr/bin/env python
# --------------------------------------------------
# IMPORT MODULES

from __future__ import division

import sys
import pygame
from pygame.locals import KEYDOWN
from display import DISPLAY

#############################
# Import colors
import colors

#############################
# Import parameters
from parameters import FPS, fullscreen_on

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

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            #
            # Quit if something goes wrong
            #
            if event.unicode == u'q':
                running = False
                pygame.quit()
                sys.exit()

