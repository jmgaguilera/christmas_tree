#!/usr/bin/python3
# -*- coding: utf-8 -*-

from com.jmgaguilera.ACME.ChristmasTree import ChristmasTree
from curses import wrapper

def main(stdscr):
    ct = ChristmasTree(stdscr, "Merry Christmas\nand\nHappy New Year", run_for=15)
    ct.run()

wrapper(main)
