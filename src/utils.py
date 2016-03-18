from __future__ import division

import os
import random
import numpy as np
from tkFileDialog import askopenfilename
from parameters import listPseudoRnd1, listPseudoRnd2, listPseudoRnd3, listPseudoRnd4, debug_mode, output_dir
from datetime import datetime


def update_center(joy_status, joy_range):
    """
    update center of the joystick
    """
    joy_range['x_center'] = joy_status['x_sensor'] / 1024
    joy_range['y_center'] = joy_status['y_sensor'] / 1024

    if debug_mode:
        print 'Center: ' + str(joy_range['x_center']) + '-' + str(joy_range['y_center'])

    return joy_range


def update_range(joy_status, joy_range):
    """
    update range of the joystick
    """

    x = joy_status['x_sensor'] / 1024
    y = joy_status['y_sensor'] / 1024

    if x < joy_range['jx_min']:
        joy_range['jx_min'] = x
    if x > joy_range['jx_max']:
        joy_range['jx_max'] = x
    if y < joy_range['jy_min']:
        joy_range['jy_min'] = y
    if y > joy_range['jy_max']:
        joy_range['jy_max'] = y

    x_cur_min = np.min([abs(joy_range['x_center'] - joy_range['jx_min']),
                        abs(joy_range['jx_max'] - joy_range['x_center'])])

    y_cur_min = np.min([abs(joy_range['y_center'] - joy_range['jy_min']),
                        abs(joy_range['jy_max'] - joy_range['y_center'])])

    if x_cur_min > joy_range['x_min_range']:
        joy_range['x_min_range'] = x_cur_min
        joy_range['x_max'] = joy_range['x_center'] + joy_range['x_min_range']
        joy_range['x_min'] = joy_range['x_center'] - joy_range['x_min_range']

    if y_cur_min > joy_range['y_min_range']:
        joy_range['y_min_range'] = y_cur_min
        joy_range['y_max'] = joy_range['y_center'] + joy_range['y_min_range']
        joy_range['y_min'] = joy_range['y_center'] - joy_range['y_min_range']

    if debug_mode:
        print 'x-range: ' + str(joy_range['x_min_range'])
        print 'y-range: ' + str(joy_range['y_min_range'])
        print 'x-min-max: ' + str(joy_range['x_min']) + '-' + str(joy_range['x_max'])
        print 'y-min-max: ' + str(joy_range['y_min']) + '-' + str(joy_range['y_max'])

    return joy_range


def scale_position_cursor(joy_range, joy_status, graph, flip=0):
    """
    scale position of the cursor depending of the flip
    """

    ttx = joy_status['x_sensor'] / 1024
    tty = joy_status['y_sensor'] / 1024
    mid_width = graph.width / 2
    mid_height = graph.height / 2

    if flip == 0:
        if ttx >= joy_range['x_max']:
            jx_scaled = graph.width
        elif ttx <= joy_range['x_min']:
            jx_scaled = 0
        elif ttx >= joy_range['x_center']:
            jx_scaled = int((ttx - joy_range['x_center']) * graph.width / (2 * joy_range['x_min_range']) + mid_width)
        else:
            jx_scaled = int(abs(ttx - joy_range['x_min']) * graph.width / (2 * joy_range['x_min_range']))

        if tty >= joy_range['y_max']:
            jy_scaled = graph.height
        elif tty <= joy_range['y_min']:
            jy_scaled = 0
        elif tty >= joy_range['y_center']:
            jy_scaled = int((tty - joy_range['y_center']) * graph.height / (2 * joy_range['y_min_range']) + mid_height)
        else:
            jy_scaled = int(abs(tty - joy_range['y_min']) * graph.height / (2 * joy_range['y_min_range']))

        joy_status['x_monitor'] = jx_scaled
        joy_status['y_monitor'] = jy_scaled

        return [jx_scaled, jy_scaled]

    if flip == 'left':
        if ttx >= joy_range['x_max']:
            jx_scaled = graph.width
        elif ttx <= joy_range['x_min']:
            jx_scaled = 0
        elif ttx >= joy_range['x_center']:
            jx_scaled = int((ttx - joy_range['x_center']) * graph.width / (2 * joy_range['x_min_range']) + mid_width)
        else:
            jx_scaled = int(abs(ttx - joy_range['x_min']) * graph.width / (2 * joy_range['x_min_range']))

        if tty >= joy_range['y_max']:
            jy_scaled = 0
        elif abs(joy_range['y_center'] - tty) >= joy_range['y_min_range']:
            jy_scaled = graph.height
        elif tty >= joy_range['y_center']:
            jy_scaled = int(abs(tty - joy_range['y_max']) * graph.height / (2 * (joy_range['y_min_range'])))
        else:
            jy_scaled = int(
                abs((joy_range['y_center'] - tty)) * graph.height / (2 * (joy_range['y_min_range'])) + mid_height)

        joy_status['x_monitor'] = jy_scaled
        joy_status['y_monitor'] = jx_scaled

        return [jy_scaled, jx_scaled]

    if flip == 'right':
        if ttx >= joy_range['x_max']:
            jx_scaled = 0
        elif ttx <= joy_range['x_min_range']:
            jx_scaled = graph.width
        elif ttx >= joy_range['x_center']:
             jx_scaled = int(
                abs((joy_range['x_max'] - ttx)) * graph.width / (2 * (joy_range['x_min_range'])))
        else:
            jx_scaled = int(
                abs((joy_range['x_center'] - ttx)) * graph.width / (2 * joy_range['x_min_range']) + mid_width)

        if tty >= joy_range['y_max']:
            jy_scaled = graph.height
        elif abs(joy_range['y_center'] - tty) >= joy_range['y_min_range']:
            jy_scaled = 0
        elif tty >= joy_range['y_center']:
            jy_scaled = int(
                abs((joy_range['y_center'] - tty)) * graph.height / (2 * joy_range['y_min_range']) + mid_height)
        else:
            jy_scaled = int(abs(tty - joy_range['y_min']) * graph.height / (2 * joy_range['y_min_range']))

        joy_status['x_monitor'] = jy_scaled
        joy_status['y_monitor'] = jx_scaled

        return [jy_scaled, jx_scaled]


def create_targets_list(param, option):
    """
    create list of targets depending of option

    option == 0 then all random
    option == 1 then all random with same number of each target
    option == 2 then sequence
    option == 3 then sequence starting at random position
    option == 4 ctrl condition even
    option == 5 ctrl condition odd
    option == 6 pseudo random
    """
    target = np.zeros(param['nbKeys'])

    if option == 0:  # all random
        target[0] = random.randrange(1, 5, 1)
        for key in range(1, param['nbKeys']):
            target[key] = random.randrange(1, 5, 1)
            while target[key - 1] == target[key]:
                target[key] = random.randrange(1, 5, 1)

    elif option == 1:  # all random with same number of each target
        target[0:4] = np.random.permutation([1, 2, 3, 4])
        for key in range(1, int(param['nbKeys'] / 4)):
            target[key * 4:(key + 1) * 4] = np.random.permutation([1, 2, 3, 4])
            while target[key * 4 - 1] == target[key * 4]:
                target[key * 4:(key + 1) * 4] = np.random.permutation([1, 2, 3, 4])

    elif option == 2:  # sequence
        nbRepetition = int(param['nbKeys'] / len(param['seqUsed']))
        target = param['seqUsed'] * nbRepetition

    elif option == 3:  # sequence starting at random position
        pos = random.randrange(1, 5, 1)
        for key in range(0, param['nbKeys']):
            target[key] = param['seqUsed'][np.mod(key + pos, len(param['seqUsed'])) - 1]

    elif option == 4:  # CTRL
        nbRepetition = int(param['nbKeys'] / len(param['seqUsed']))
        target = param['seq_ctrl_used_bloc_even'] * nbRepetition

    elif option == 5:  # CTRL ODD
        nbRepetition = int(param['nbKeys'] / len(param['seqUsed']))
        target = param['seq_ctrl_used_bloc_odd'] * nbRepetition

    elif option == 6:  # PSEUDO RANDOM
        tmpRnd = random.randint(1, 4)
        if tmpRnd == 1:
            target = listPseudoRnd1
        elif tmpRnd == 2:
            target = listPseudoRnd2
        elif tmpRnd == 3:
            target = listPseudoRnd3
        else:
            target = listPseudoRnd4
    return target


def extract_RT_feedback(targets, min_median_ref, param):
    """
    extract rt to give feedback
    """

    reaction_time = []

    for i in range(param['nbKeys']):
        reaction_time.append(
            (targets[i * 2 + 1] - targets[i * 2]).total_seconds())

    targets = []

    # Remove first value
    reaction_time = reaction_time[1:]

    value_inf_median = [x for x in reaction_time if x < min_median_ref]

    if np.median(reaction_time[1:]) < min_median_ref:
        min_median_ref = (np.median(reaction_time[1:]) + min_median_ref) / 2

    return [targets, min_median_ref, value_inf_median]


def extract_min_rt(subject_id, logfilename, param):
    """
    extraction min reaction time
    """

    [infos, key] = read_log(logfilename)

    if debug_mode:
        print 'Infos_description: '+str(infos['description'])
        print 'Logfilename: '+str(logfilename)


    all_rt = []

    indexes_target_start = [i for i, x in enumerate(infos['description']) if x == "Target drawn"]
    indexes_target_end = [i for i, x in enumerate(infos['description']) if x == "Target end"]

    if debug_mode:
        print 'len(indexes_target_end): '+str(len(indexes_target_end))
        print 'len(indexes_target_start): '+str(len(indexes_target_start))

    if len(indexes_target_start) == len(indexes_target_end):
        for index in range(len(indexes_target_start)):
            start = indexes_target_start[index]
            end = indexes_target_end[index]
            # diff btw Target end and Target drawn - param['time_target']
            all_rt.append((infos['time'][end] - infos['time'][start]).total_seconds() - param['time_target'])

    if debug_mode:
        print 'Size: ' + str(len(all_rt))
        print all_rt


    #
    # all rt
    #
    matrix_rt = np.reshape(all_rt, (param['nbBlocs'], param['nbKeys']))

    if debug_mode:
        print('Matrix RT reshaped')
        print matrix_rt
    #
    # Compute median rt of each bloc
    #
    median_matrix_RT = []
    for numBloc in range(param['nbBlocs']):
        current_bloc = matrix_rt[numBloc][:]

        if debug_mode:
            print 'bloc: ' + str(numBloc)
            print current_bloc

        median_matrix_RT.append(np.median(current_bloc[1:]))

    #
    # 2 lowest values if more than 2 blocs
    #
    value_for_avering = []
    if param['nbBlocs'] > 2:
        for i in range(2):
            value_for_avering.append(min(median_matrix_RT))
            median_matrix_RT.remove(min(median_matrix_RT))
    else:
        value_for_avering = median_matrix_RT

    #
    # save min rt into a log file
    #
    rt_filename = os.getcwd() + os.sep + 'min.rt'

    output_rt = open(rt_filename, 'w')
    output_rt.write(str(np.mean(value_for_avering)))
    output_rt.close()


def read_log(logfilename):
    """
    read logfile
    """
    infos = {}

    log = open(logfilename, 'r')

    for numline, line in enumerate(log):
        if numline == 12:
            keys = line.split(',')
            del keys[-1]  # remove last comma
            for key in keys:
                infos[key] = []

            if debug_mode:
                print(infos)

        if numline > 12:
            line = line.split(',')
            del line[-1]  # remove last comma

            for numkey, val in enumerate(line):
                if keys[numkey] == 'description':
                    infos[keys[numkey]].append(str(val))

                elif keys[numkey] == 'time':
                    infos[keys[numkey]].append(datetime.strptime(val, "%H:%M:%S.%f"))

                elif keys[numkey] == 'ttl':
                    infos[keys[numkey]].append(val)

                else:
                    infos[keys[numkey]].append(float(val))

    log.close()

    # TODO: CHECK if same size infos['keys']
    return infos, keys


def log_header(logfile, joy_status, task_info, joy_range=0, min_rt=0):
    """
    create header for the logfile
    """

    if not joy_range==0:
        for key, val in joy_range.items():
            logfile.write("%s:%s\n" % (str(key), str(val)))

    if not min_rt==0:
        logfile.write("min_rt:%s\n" % str(min_rt))

    for key, val in joy_status.items():
        logfile.write(str(key) + ',')

    for key, val in task_info.items():
        logfile.write(str(key) + ',')

    logfile.write('\n')


def log(logfile, joy_status, task_info):
    """
    log joy_status and task_info in a logfile
    """

    for key, val in joy_status.items():
        logfile.write(str(val) + ',')

    for key, val in task_info.items():
        logfile.write(str(val) + ',')

    logfile.write('\n')


def get_logfile(subject_id, task):
    """
    find an new name that doesn't already exist
    """

    i = 1
    prefix = output_dir + subject_id + '_' + task + '_'

    logfilename = prefix + str(i) + '.txt'
    while os.path.exists(logfilename):
        i += 1
        logfilename = prefix + str(i) + '.txt'

    return logfilename


def save_calibration(subject_id, joy_range):
    """
    save joy_range for next calibration - use of jr (joy_range) extension
    """
    logfile = os.getcwd() + os.sep + 'calibration.jr'

    f = open(logfile, 'w')

    for key, val in joy_range.items():
        f.write("%s:%s\n" % (str(key), str(val)))

    f.close()


def load_calibration():
    """
    load calibration
    """
    joy_range = {}

    calibration_file = os.getcwd() + os.sep + 'calibration.jr'

    fc = open(calibration_file)

    for line in fc:
        line = line.split(':')
        joy_range[line[0]] = float(line[1])

    if debug_mode:
        print(joy_range)

    return joy_range


def save_emg_calibration(rt_plot):
    """
    save joy_range for next calibration - use of jr (joy_range) extension
    """
    logfile = os.getcwd() + os.sep + 'calibration.emg'
    print logfile

    f = open(logfile, 'w')

    f.write("%s:%f\n" % ('min', rt_plot.min))
    f.write("%s:%f\n" % ('max', rt_plot.max))

    f.close()


def load_emg_calibration():
    """
    load calibration
    """
    calibration_file = os.getcwd() + os.sep + 'calibration.emg'

    fc = open(calibration_file)
    line = fc.readline()
    line = line.split(':')
    rt_min = float(line[1])
    line = fc.readline()
    line = line.split(':')
    rt_max = float(line[1])

    if debug_mode:
        print([rt_min, rt_max])

    return [rt_min, rt_max]


def get_min_rt_from_rtfile(subject_id):
    """
    get rt file from training
    :param subject_id:
    :return: min_median_ref
    """
    training_rt_file = os.getcwd() + os.sep + 'min.rt'

    g = open(training_rt_file)

    for line in g:
        min_median_ref = float(line)

    g.close()

    return min_median_ref


def check_event_learning():
    key_pressed = False
    while not key_pressed:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                ################
                # Quit if something goes wrong
                if event.unicode == u'q':
                    running = False
                    quit()
                    sys.exit()
                if event.unicode == u'1':
                    return 1
                    key_pressed = True
                elif event.unicode == u'2':
                    return 2
                    key_pressed = True
                elif event.unicode == u'3':
                    return 3
                    key_pressed = True
                else:
                    key_pressed = False

