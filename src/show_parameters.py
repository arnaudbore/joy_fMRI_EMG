#!/usr/bin/env python
# --------------------------------------------------
# IMPORT MODULES

import sys, os
sys.path.append(os.getcwd())
from parameters import *

print '\n'
print '########################'
print '# Parameters'
print '#'
print '# Flip joystick: '+ str(flip)
print '#'
print '# Screen:'
print '#    window_width: '+str(window_width)
print '#    window_height: '+str(window_height)
print '#    size_target: '+str(size_target)
print '#    size_cursor: '+str(size_cursor)
print '#'
print '#'
print '# Parameters for the task'
print '# '+str(param_task)
print '#'
print '# Parameters for the training'
print '# '+str(param_training)
print '#'
print '# Fullscreen : '+str(fullscreen_on)
print '#'
print '# EMG start : '+str(EMG_start)
print '#'
print '# Wait for MRI for the task : '+str(irm)
print '#'
print '# Wait for MRI for the training : '+str(irm_training)
print '#'
print '########################'
print '\n'
print '\n'
print '\n'
