#
# abore: 26-03-15
# parameter file for task/training joystick

# Debug mode
debug_mode = False

###################################
# Labjack parameters
#
# DON'T MODIFY THIS SECTION !!!
#

# Trigger EMG recording
lj_trigger_emg = {'channel': 7}

# Trigger stimulation bloc during rest period of the task
lj_trigger_stim = {'channel': 5}

# Receive signal when it's the end of a stimulation bloc
lj_end_stim = {'channel': 4}

# Monitor EMGtt
lj_monitor_emg = {'channel': 1}


###################################
###################################
#
# General Task-Training-Calibration parameters
#
###################################
###################################

#
# Structure used to share information about the task/training
#
task_info = {'numTarget': 0,
             'numBloc': 0,
             'numKey': 0,
             'numBloc_rest': 0,
             'time': None,
             'position_target': 0,
             'description': 'Joystick_movement'}

# French 1, English 0
language = 1

# fullscreen
if debug_mode:
    fullscreen_on = False  # False or True
else:
    fullscreen_on = True  # False or True

# Mirror Screen
mirrorScreen = False

# Folder where to save logs
output_dir = '/home/labdoyon/Documents/PycharmProjects/Stimulation_Data/'

# Flip clock wise joystick
flip = 'left'  # or 0, 'left' or 'right'

#
# pygame information
#

# window size
window_width = 512
window_height = 512

# objects size
size_target = 36#24
size_cursor = 22#20

# margins size
margin_targets = 18 + size_target #16 + size_target

# positions targets
positions_target = [(0, 0),
                    # mid left
                    (margin_targets,
                     int(window_height / 2)),
                    # mid bottom
                    (int(window_width / 2),
                     window_height - margin_targets),
                    # mid top
                    (int(window_width / 2),
                     margin_targets),
                    # mid right
                    (window_width - margin_targets,
                     int(window_height / 2))
                    ]

# Frame per seconds
FPS = 1000  # frames per second setting

#
# Calibration
#
joy_range = {'jx_min': 0.55,
             'jx_max': 0.55,
             'jy_min': 0.55,
             'jy_max': 0.55,
             'x_min': 0,
             'x_max': 0,
             'x_min_range': 0,
             'y_max': 0,
             'y_min': 0,
             'y_min_range': 0,
             'x_center': 0.5,
             'y_center': 0.5}

calibration_string = ['CENTER', 'UP', 'DOWN', 'LEFT', 'RIGHT']

####################################
# PARAMETERS TASK
param_task = {'nbKeys': 80, # 8
              'seqUsed': [1, 2, 3, 1, 4, 2, 4, 3],
              'seq_ctrl_used_bloc_even': [2, 3, 2, 3, 2, 3, 2, 3],
              'seq_ctrl_used_bloc_odd': [1, 4, 1, 4, 1, 4, 1, 4],
              'nbBlocs': 15, # 16
              'rest_time': 15,  # 5
              'time_target': 0.005,
              'numBloc_Reststim': [1, 2, 14, 15],
              'numBloc_EMGmonitor': [1, 14],
              'mri_trigger': False,
              'run_stimulation': True,
              'start_emg': True,
              'monitor_emg': True,
              'feedback': False}


list_seq_recognition = [[1, 2, 3, 1, 4, 2, 3, 4],
                        [1, 2, 3, 4, 1, 2, 4, 3],
                        [1, 2, 3, 1, 4, 2, 4, 3],
                        [1, 2, 3, 2, 4, 1, 4, 3],
                        [1, 2, 3, 1, 4, 2, 4, 3],
                        [1, 2, 3, 1, 4, 3, 4, 2]]

listPseudoRnd1 = [3, 1, 4, 3, 2, 4, 1, 3, 1, 2, 4, 1, 3, 4, 2, 3, 1, 2, 4, 2,
                  1, 3, 4, 2, 3, 4, 2, 1, 3, 2, 4, 1, 3, 1, 2, 4, 3, 2, 4, 1,
                  4, 1, 3, 2, 1, 2, 3, 4, 1, 2, 1, 3, 2, 3, 4, 2, 4, 1, 3, 2,
                  1, 3, 1, 4, 2, 3, 1, 2, 4, 2, 3, 4, 3, 1, 2, 4, 3, 4, 2, 1]


listPseudoRnd2 = [1, 4, 2, 3, 4, 2, 1, 3, 1, 4, 2, 3, 1, 2, 4, 3, 2, 4, 3, 1,
                  2, 4, 2, 1, 3, 2, 4, 3, 1, 4, 2, 1, 3, 1, 4, 2, 3, 4, 1, 3,
                  1, 2, 4, 3, 4, 2, 1, 3, 4, 3, 2, 4, 2, 1, 3, 2, 4, 1, 3, 1,
                  2, 3, 1, 4, 2, 4, 3, 2, 3, 1, 2, 1, 4, 3, 2, 1, 2, 3, 1, 4]

listPseudoRnd3 = [1, 4, 2, 3, 4, 2, 1, 3, 1, 4, 2, 3, 1, 2, 4, 3, 2, 4, 3, 1,
                  2, 4, 2, 1, 3, 2, 4, 3, 1, 4, 2, 1, 3, 1, 4, 2, 3, 4, 1, 3,
                  4, 1, 3, 2, 1, 2, 3, 4, 1, 2, 1, 3, 2, 3, 4, 2, 4, 1, 3, 2,
                  1, 3, 1, 4, 2, 3, 1, 2, 4, 2, 3, 4, 3, 1, 2, 4, 3, 4, 2, 1]

listPseudoRnd4 = [1, 2, 4, 3, 4, 2, 1, 3, 4, 3, 2, 4, 2, 1, 3, 2, 4, 1, 3, 1,
                  2, 3, 1, 4, 2, 4, 3, 2, 3, 1, 2, 1, 4, 3, 2, 1, 2, 3, 1, 4,
                  3, 1, 4, 3, 2, 4, 1, 3, 1, 2, 4, 1, 3, 4, 2, 3, 1, 2, 4, 2,
                  1, 3, 4, 2, 3, 4, 2, 1, 3, 2, 4, 1, 3, 1, 2, 4, 3, 2, 4, 1]

##############################
# PARAMETERS TRAINING

param_training = {'nbKeys': 80, # 80
                  'nbBlocs': 7, # 7
                  'rest_time': 5,  # 15
                  'time_target': 0.005,
                  'mri_trigger': False,
                  'start_mri': False,
                  'run_stimulation': True,
                  'monitor_emg': False,
                  'start_emg': True}

##############################
# PARAMETERS RECOGNITION
list_seq_recognition = [[1, 2, 3, 1, 4, 2, 3, 4],
                        [1, 2, 3, 4, 1, 2, 4, 3],
                        [1, 2, 3, 1, 4, 2, 4, 3],
                        [1, 2, 3, 2, 4, 1, 4, 3],
                        [1, 2, 3, 1, 4, 2, 4, 3],
                        [1, 2, 3, 1, 4, 3, 4, 2]]

##############################
# PARAMETERS EMG STIMULATION AND MONITORING

emg_buffer = 500 # number of data points needed to calculate integral
emg_max_value2plot = 0.30 # max value to plot so we can see
