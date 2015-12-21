#!/usr/bin/python3
# -*- coding: utf-8 -*-

import curses
import time
import random

class ChristmasTree:

    def __init__(self, stdscr, message='Merry Christmas',
            star_delay = 1, # bigger -> slow blink
            light_delay = 4,# bigger -> slow blink
            light_density = 6, # bigger -> less density
            run_for = 10):
        self.stdscr = stdscr
        self.message = message
        self.star_delay = star_delay
        self.star_count = 0
        self.light_delay = light_delay
        self.light_count = 0
        self.light_density = light_density
        self.run_for = run_for

    def run(self):
        self._init_all()
        self._prepare_tree()
        self._prepare_message()
        for i in range(0, self.run_for):
            self._prepare_star()
            self._prepare_light()
            self._draw_all()
            time.sleep(1)

    def _init_all(self):
        self.screen = [[' ' for x in range(0, curses.COLS)]
                        for x in range(0, curses.LINES)]
        self.scr_color = [[1 for x in range(0, curses.COLS)]
                        for x in range(0, curses.LINES)]
        self.light = [] # no balls at start
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)


    _star = [['   |   ',
             '  \|/  ',
             '--=O=--',
             '  /|\  ',
             '   |   '],
             [[1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1],
              [1,1,1,2,1,1,1],
              [1,1,1,1,1,1,1],
              [1,1,1,1,1,1,1]
             ]]

    def _prepare_star(self):
        Y = int(curses.COLS / 2) - int(len(self._star[0][0])/2)-1

        self.star_count += 1
        if self.star_count > self.star_delay:
            self.star_count = 0

        for x in range(0, len(self._star[0])):
            for z in range(0, len(self._star[0][x])):
                self.screen[x][Y+z] = self._star[0][x][z]
                self.scr_color[x][Y+z] = self._star[1][x][z]
                if self.star_count == 0:
                    if self._star[1][x][z] == 1:
                        self._star[1][x][z] = 2
                    else:
                        self._star[1][x][z] = 1

    def _prepare_tree(self):
        Y = int(curses.COLS / 2) - 1;
        self.space_tree = 0
        for x in range(4, curses.LINES-4, 4):
            pos1 = Y - (x - 4)
            pos2 = Y + (x - 4)
            for y in range(0,4):
                self.screen[x+y][pos1-y*2] = '/'
                self.screen[x+y][pos2+y*2] = '\\'
                self.scr_color[x+y][pos1-y*2] = 5; # GREEN
                self.scr_color[x+y][pos2+y*2] = 5; # GREEN

        self.space_tree = 0
        for x in range(4, curses.LINES-1):
            in_tree = False
            for y in range(0, curses.COLS-1):
                if self.screen[x][y] == '/':
                    in_tree = True
                elif self.screen[x][y] == '\\':
                    in_tree = False
                elif in_tree:
                    self.space_tree += 1

        self.max_light = int(self.space_tree / self.light_density)

    def _prepare_light(self):
        # create new lights
        if len(self.light) < self.max_light:
            for i in range(0, self.max_light-len(self.light)):
                light_type = ('*' if random.randint(0,1)==0 else 'O')
                light_color = random.randint(1,4)
                light_position = random.randint(1,self.space_tree)
                self.light.append([light_type,
                                    light_color, light_position])
            self.light=sorted(self.light, key=lambda x: x[2])
        # position lights
        step_in_tree_space = 1
        step_in_light = 0
        for x in range(4, curses.LINES-1):
            in_tree = False
            for y in range(0, curses.COLS-1):
                if self.screen[x][y] == '/':
                    in_tree = True
                elif self.screen[x][y] == "\\":
                    in_tree = False
                elif in_tree:
                    self.screen[x][y] = ' '
                    self.scr_color[x][y] = 1
                    while (step_in_light < len(self.light) and
                            self.light[step_in_light][2] == step_in_tree_space):
                        self.screen[x][y] = self.light[step_in_light][0]
                        self.scr_color[x][y] = self.light[step_in_light][1]
                        step_in_light += 1
                    step_in_tree_space += 1
        # remove some lights (use light_delay)
        for i in range(0, int(len(self.light) / self.light_delay)):
            x = random.randint(0, len(self.light)-1)
            self.light.pop(x)

    def _prepare_message(self):
        self.messages = self.message.split('\n')

    def _draw_all(self):
        #self.stdscr.addstr(str(",".join([str(x[0]) for x in self.light])))
        #self.stdscr.refresh()
        #time.sleep(3)
        for x in range(0, curses.LINES-1):
            for y in range(0, curses.COLS-1):
                self.stdscr.addstr(x,y,self.screen[x][y],
                        curses.color_pair(self.scr_color[x][y]))
        i = 0
        for x in range(len(self.messages), 0, -1):
            self.stdscr.addstr(curses.LINES-1-x,
                int(curses.COLS/2-(len(self.messages[i])+2)/2),
                            " " + self.messages[i] + " ")
            i += 1

        self.stdscr.refresh()
