#!/usr/bin/env python

from curses import *
import string

line = -1 # line of the prompt

scr = None

lines = None
cols = None

white = None
yellow = None
cyan = None
magenta = None
green = None
red = None

def openline():
    global scr, lines, line
    if line == lines - 1:
        scr.scroll()
    else:
        line += 1
    lastline()

def messageline():
    global line, scr
    openline()
    scr.move(line-1, 0)
    scr.insertln()

def overwriteline():
    global scr
    y, x = scr.getyx()
    scr.move(y, 0)
    scr.deleteln()
    scr.insertln()

def lastline():
    global scr, line
    scr.move(line, 0)

def removelastline():
    global scr, line
    lastline()
    scr.deleteln()
    line -= 1
    lastline()

def clearscreen():
    global scr, line
    line = -1
    scr.clear()
    openline()

def init():
    global scr, lines, cols, white, yellow, cyan, magenta, green, red
    scr = initscr()
    noecho()
    cbreak()
    curs_set(0)
    scr.keypad(1)
    scr.scrollok(1)
    lines, cols = scr.getmaxyx()
    start_color()
    init_pair(1, COLOR_YELLOW, COLOR_BLACK)
    init_pair(2, COLOR_CYAN, COLOR_BLACK)
    init_pair(3, COLOR_MAGENTA, COLOR_BLACK)
    init_pair(4, COLOR_GREEN, COLOR_BLACK)
    init_pair(5, COLOR_RED, COLOR_BLACK)
    white = color_pair(0)
    yellow = color_pair(1)
    cyan = color_pair(2)
    magenta = color_pair(3)
    green = color_pair(4)
    red = color_pair(5)
    openline()
    scr.addstr("Hottest cats on the block", A_BOLD)
    openline()
    scr.addstr("A gamejam game about hackers")
    openline()
    scr.addstr("by Felix Schneider")
    openline()
    scr.refresh()

def uninit():
    global scr
    echo()
    nocbreak()
    scr.keypad(0)
    curs_set(1)
    endwin()

lastinput = ""

def getline(ch = None):
    global scr, lastinput
    buff = []
    sy, sx = scr.getyx()
    curs_set(1)
    flushinp()
    while True:
        c = scr.getch()
        y, x = scr.getyx()
        if c == 10:
            break
        elif (c == KEY_BACKSPACE or c == ord('\b')) and x > sx:
            scr.addstr(y, x - 1, scr.instr(len(buff) - (x-sx)).decode('ascii'))
            scr.delch(y, sx + len(buff)-1)
            del buff[x-1-sx]
            scr.move(y, x-1)
        elif c == KEY_LEFT and x > sx:
            scr.move(y, x-1)
        elif c == KEY_RIGHT and x < sx + len(buff):
            scr.move(y, x+1)
        elif c == KEY_UP:
            scr.addstr(sy, sx, " " * len(buff))
            del buff[:]
            scr.move(sy, sx)
            for cha in lastinput:
                buff.append(cha)
                scr.addch(ord(cha))
            if x - sx < len(buff):
                scr.move(y, x)
        elif c == KEY_DOWN:
            scr.addstr(sy, sx, " " * len(buff))
            del buff[:]
            scr.move(sy, sx)
        elif c == KEY_END:
            scr.move(y, sx + len(buff))
        elif c == KEY_HOME:
            scr.move(y, sx)
        elif c == KEY_DC and x < sx + len(buff):
            scr.addstr(y, x, scr.instr(y, x+1, len(buff) - (x-sx+1)))
            scr.delch(y, sx + len(buff)-1)
            del buff[x-sx]
            scr.move(y,x)
        elif c < 127 and chr(c) in string.printable:
            buff.insert(x-sx+1, chr(c))
            if ch == None:
                scr.insch(c)
            else:
                scr.insch(ord(ch))
            scr.move(y,x+1)
    curs_set(0)
    res = "".join(buff)
    lastinput = res
    return res
