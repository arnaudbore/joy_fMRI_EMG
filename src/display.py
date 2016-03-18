from __future__ import division
from pygame.locals import FULLSCREEN
import pygame
from pygame.locals import KEYDOWN
import colors
import math
import numpy as np
from datetime import datetime
from datetime import timedelta
import sys
from utils import scale_position_cursor, log, load_emg_calibration
from parameters import positions_target, size_cursor, size_target, window_width, window_height, \
    param_training, flip, lj_monitor_emg, lj_end_stim, \
    emg_max_value2plot, emg_buffer, mirrorScreen

import os

from point import Point


class DISPLAY(object):
    def __init__(self, descriptive_text=None, joy_thread=None, task_info=None, FPS=100, fullscreen=None, debug=False):
        self.descriptive_text = descriptive_text
        self.joy_thread = joy_thread
        self.task_info = task_info
        self.window = pygame.Rect(0, 0, window_width, window_height)
        self.debug = debug
        self.fpsClock = pygame.time.Clock()
        self.FPS = FPS
        self.log_start_bloc = False
        self.need_display_target = True
        self.targets_start_end = []

        if fullscreen:
            self.display = pygame.display.set_mode((self.window.width, self.window.height), FULLSCREEN)
        else:
            self.display = pygame.display.set_mode((self.window.width, self.window.height))

        pygame.display.init()
        pygame.font.init()

        # Title
        caption = "JOYSTICK - TASK"
        pygame.display.set_caption(caption)
        # Hide mouse
        pygame.mouse.set_visible(False)


        ### SCREEN MIRRORED
        if mirrorScreen:
            os.system('xrandr --output DP1 --reflect x')

    def target_found(self, start_target_found):

        jx_scaled = self.joy_thread.joy_status['x_monitor']
        jy_scaled = self.joy_thread.joy_status['y_monitor']

        target_scaled = positions_target[self.task_info['position_target']]

        if math.sqrt(math.pow((jx_scaled - target_scaled[0]), 2) +
                      math.pow((jy_scaled - target_scaled[1]), 2)) - size_cursor <= size_target:

            if self.debug:
                print 'Target found'

            if not start_target_found:
                self.task_info['description'] = 'Target reached'
                self.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
                log(self.joy_thread.logfile, self.joy_thread.joy_status, self.task_info)

            return True

    def display_edges(self):
        pygame.draw.rect(
            self.display, colors.WHITE, (0, 0, self.window.width, self.window.height), 5)

    def display_target(self, write_log=False):
        # 1 - GAUCHE
        # 2 - BAS
        # 3 - HAUT
        # 4 - DROITE
        if self.task_info['position_target'] > 0:
            pygame.draw.circle(self.display, colors.GREEN, positions_target[self.task_info['position_target']],
                               size_target)

            if self.debug:
                print('Position_target: %s' % (str(positions_target[self.task_info['position_target']])))

            if self.need_display_target:
                self.task_info['description'] = 'Target drawn'
                self.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
                #
                # self.targets_start_end to compute feedback information
                #
                self.targets_start_end.append(datetime.now())
                if write_log:
                    log(self.joy_thread.logfile, self.joy_thread.joy_status, self.task_info)

                self.need_display_target = False

    def display_all_targets(self):
        self.display.fill(colors.BLACK)
        pygame.draw.circle(
            self.display, colors.RED, positions_target[1], size_target)
        pygame.draw.circle(
            self.display, colors.RED, positions_target[2], size_target)
        pygame.draw.circle(
            self.display, colors.RED, positions_target[3], size_target)
        pygame.draw.circle(
            self.display, colors.RED, positions_target[4], size_target)

    def display_cursor(self):
        [jx_scaled, jy_scaled] = scale_position_cursor(self.joy_thread.joy_range,
                                                       self.joy_thread.joy_status,
                                                       self.window,
                                                       flip)

        self.joy_thread.joy_status['x_monitor'] = jx_scaled
        self.joy_thread.joy_status['y_monitor'] = jy_scaled

        if self.debug:
            print('x_monitor,y_monitor: %s-%s' % (str(jx_scaled), str(jy_scaled)))

        self.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
        self.task_info['description'] = 'joystick movement'
        log(self.joy_thread.logfile, self.joy_thread.joy_status, self.task_info)

        pygame.draw.circle(
            self.display, colors.GREEN, (jx_scaled, jy_scaled), size_cursor)

    def display_text(self,
                     text,
                     color,
                     size_text,
                     start=datetime.now().strftime("%H:%M:%S.%f"),
                     duration=3600,
                     question=False,
                     write_log=True):

        # CROSS AT THE CENTER
        font = pygame.font.Font(None, size_text)
        text_to_render = font.render(text, 1, color)
        if self.debug:
            print 'width,height = ' + str(text_to_render.get_width()) + ' , ' + str(text_to_render.get_height()) + '\n'
        if duration != 3600:
            while datetime.now() < start + timedelta(seconds=duration):

                if text == ' + ': # Works only with display_rest
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                        #
                        # Quit if something goes wrong
                        #
                            if event.unicode == u'q':
                                running = False
                                pygame.quit()
                                sys.exit()


                if text_to_render.get_width() < window_width:

                    if text is '+':
                        self.display_all_targets()

                        self.display.blit(
                            text_to_render,
                            (self.window.width / 2 - text_to_render.get_width() / 2,
                             self.window.height / 2 - text_to_render.get_height() / 2))

                    else:
                        self.display.fill(colors.BLACK)
                        self.display.blit(
                            text_to_render,
                            (self.window.width / 2 - text_to_render.get_width() / 2,
                             self.window.height / 2 - text_to_render.get_height() / 2))

                    self.update()
                else:
                    if len(text.split('  ')) == 2:
                        line1_to_render = font.render(text.split('  ')[0], 1, color)
                        line2_to_render = font.render(text.split('  ')[1], 1, color)
                        self.display.fill(colors.BLACK)
                        self.display.blit(
                            line1_to_render,
                            (self.window.width / 2 - line1_to_render.get_width() / 2,
                             self.window.height / 3 - line1_to_render.get_height() / 2))

                        self.display.blit(
                            line2_to_render,
                            (self.window.width / 2 - line2_to_render.get_width() / 2,
                             self.window.height * 2 / 3 - line2_to_render.get_height() / 2))

                        self.update()
        else:
            if text_to_render.get_width() < window_width:

                if text is '+':
                    self.display_all_targets()

                    self.display.blit(text_to_render,
                                      (self.window.width / 2 - text_to_render.get_width() / 2,
                                       self.window.height / 2 - text_to_render.get_height() / 2))

                else:
                    self.display.fill(colors.BLACK)
                    self.display.blit(
                        text_to_render,
                        (self.window.width / 2 - text_to_render.get_width() / 2,
                         self.window.height / 2 - text_to_render.get_height() / 2))

                self.update()
            else:
                if len(text.split('  ')) == 2:
                    line1_to_render = font.render(text.split('  ')[0], 1, color)
                    line2_to_render = font.render(text.split('  ')[1], 1, color)
                    self.display.fill(colors.BLACK)
                    self.display.blit(
                        line1_to_render,
                        (self.window.width / 2 - line1_to_render.get_width() / 2,
                         self.window.height / 3 - line1_to_render.get_height() / 2))

                    self.display.blit(
                        line2_to_render,
                        (self.window.width / 2 - line2_to_render.get_width() / 2,
                         self.window.height * 2 / 3 - line2_to_render.get_height() / 2))

                    self.update()

        if duration == param_training['rest_time'] and write_log:
            self.task_info['time'] = start.strftime("%H:%M:%S.%f")
            self.task_info['description'] = 'start rest'
            log(self.joy_thread.logfile, self.joy_thread.joy_status, self.task_info)

            self.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
            self.task_info['description'] = 'end rest'
            log(self.joy_thread.logfile, self.joy_thread.joy_status, self.task_info)

        if question:
            return self.check_event_question()

    def display_rest(self,
                     text,
                     color,
                     size_text,
                     start=datetime.now().strftime("%H:%M:%S.%f"),
                     param=None,
                     write_log=True):

        # TEXT AT THE CENTER
        font = pygame.font.Font(None, size_text)
        text_to_render = font.render(text, 1, color)
        self.task_info['time'] = start.strftime("%H:%M:%S.%f")
        self.task_info['description'] = 'start rest'

        if write_log:
            log(self.joy_thread.logfile, self.joy_thread.joy_status, self.task_info)

        from labjack_interface import read_digital
        import lji_realtime as lji_rt

        if param['monitor_emg'] and self.task_info['numBloc_rest'] in param['numBloc_EMGmonitor']:
            #
            #   EMG plot Real Time
            #

            rt_plot = lji_rt.AnalogPlot(lj_monitor_emg, emg_buffer, self.debug)
            #
            # get EMG information
            #
            [rt_plot.min, rt_plot.max] = load_emg_calibration()

            self.task_info['rt_emg_min'] = rt_plot.min
            self.task_info['rt_emg_max'] = rt_plot.max

            while read_digital(lj_end_stim) == 0:

                if self.debug:
                    print('Read EMG : ' + str(read_digital(lj_end_stim)))

                self.display.fill(colors.BLACK)
                self.display_monitor_emg(rt_plot)
                pygame.display.update()
        else:
            while read_digital(lj_end_stim) == 0:
                self.display.blit(text_to_render,
                                  (self.window.width / 2 - text_to_render.get_width() / 2,
                                   self.window.height / 2 - text_to_render.get_height() / 2))

                pygame.display.update()

        self.task_info['time'] = datetime.now().strftime("%H:%M:%S.%f")
        self.task_info['description'] = 'end rest'
        if write_log:
            log(self.joy_thread.logfile, self.joy_thread.joy_status, self.task_info)

    def display_monitor_emg(self, rt_plot, get_minmax=False):

        while rt_plot.buff.count(0):
            rt_plot.update(get_minmax)

        rt_plot.update(get_minmax)

        current_val = float('NaN')

        while np.isnan(current_val):
            val = np.trapz(np.abs(rt_plot.buff))
            current_val = np.divide(val - rt_plot.min, rt_plot.max - rt_plot.min)

        if self.debug:
            print 'EMG value : ' + str(current_val)

        pygame.draw.rect(self.display, colors.WHITE,
                         (window_width / 4, window_height / 4, window_width / 2, window_height / 2), 0)

        if not get_minmax:
            pygame.draw.rect(self.display, colors.LIGHTGRAY,
                             (window_width / 4,
                              window_height / 2 - (window_height / 30),
                              window_width / 2,
                              window_height / 15))

        if current_val >= emg_max_value2plot:
            pygame.draw.rect(self.display, colors.BLUE,
                             (window_width / 3,
                              window_height / 4,
                              window_width / 3,
                              window_height / 4 + window_height / 2))
        else:
            pygame.draw.rect(self.display, colors.BLUE,
                             (window_width / 3,
                              window_height / 4 + (1 - np.divide(current_val, emg_max_value2plot)) * window_height / 2,
                              window_width / 3,
                              window_height / 4 + window_height / 2))

        if not get_minmax:
            self.draw_dashed_line(colors.RED,
                                  (window_width / 4, window_height / 2),
                                  (window_width * 3 / 4, window_height / 2))

        pygame.draw.rect(self.display, colors.BLACK,
                         (0,
                          window_height * 3 / 4,
                          window_width,
                          window_height / 4))

        self.display_edges()

    def display_sequence(self, sequence, len_seqUsed):
        self.display_all_targets()
        repeat_sequence = True

        target = 0
        while repeat_sequence:
            self.display_all_targets()
            # Get position of the target
            self.task_info['position_target'] = sequence[target]
            self.display_target(True)
            self.update()
            start = datetime.now()
            while datetime.now() < start + timedelta(seconds=1):
                pass

            self.display.fill(colors.BLACK)

            target += 1
            if target >= len_seqUsed:
                repeat_sequence = False

    def update(self):
        pygame.display.update()
        self.fpsClock.tick(self.FPS)

    def quit(self):
        pygame.quit()

    def check_event_question(self):
        key_pressed = False
        while not key_pressed:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.unicode == u'q':
                        key_pressed = True
                        pygame.quit()
                        sys.exit()
                    ################
                    # Quit if something goes wrong
                    elif event.unicode == u'n':
                        key_pressed = True
                        return False
                    elif event.unicode == u'y':
                        key_pressed = True
                        return True
                    elif event.unicode == u'r':
                        key_pressed = True
                        return 'r'

    def draw_dashed_line(self, color, start_pos, end_pos, width=1, dash_length=10):
        origin = Point(start_pos)
        target = Point(end_pos)
        displacement = target - origin
        length = len(displacement)
        slope = displacement.__div__(length)

        for index in range(0, int(length / dash_length), 2):
            start = origin + (slope * index * dash_length)
            end = origin + (slope * (index + 1) * dash_length)
            pygame.draw.line(self.display, color, start.get(), end.get(), width)
