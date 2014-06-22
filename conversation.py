#!/usr/bin/env python

import curses, output
import output

class Conversation:
    def __init__(self, data):
        self.data = data
        # Data is Tuples: (Sender/None, message)
    
    def run(self):
        curses.cbreak()
        curses.noecho()
        output.lastline()
        output.overwriteline()
        self.prompt()
        output.scr.refresh()
        last = None
        for item in self.data:
            if item[0] != None:
                if last != None:
                    curses.napms(600 + len(last)*30)
                else:
                    curses.napms(1000)
                self.receive(item[0], item[1])
                output.scr.refresh()
                last = item[1]
            else:
                self.send(item[1])
                output.openline()
                self.prompt()
                output.scr.refresh()
                last = None
        output.removelastline()
    
    def prompt(self):
        scr = output.scr
        scr.addstr("Type ", output.white)
        scr.addstr("message", output.yellow | curses.A_BOLD)
        scr.addstr("> ", output.white)
        
    
    def send(self, msg):
        curses.curs_set(1)
        scr = output.scr
        output.lastline()
        self.prompt()
        curses.flushinp()
        for c in msg:
            # take out for release
#            if scr.getch() == ord('\n'):
#               break
            scr.getch()
            scr.addch(c)
        while scr.getch() != ord('\n'):
            pass
        output.overwriteline()
        scr.addstr("Sent: ", output.yellow | curses.A_BOLD)
        scr.addstr(msg, output.white)
        scr.refresh()
        curses.curs_set(0)
    
    def receive(self, sender, msg):
        scr = output.scr
        output.messageline()
        scr.addstr("Incoming message from %s" % sender, output.white | curses.A_DIM)
        scr.refresh()
        curses.napms(1000 + len(msg)*10)
        output.overwriteline()
        scr.addstr(sender, curses.color_pair(hash(sender) % 5 + 1))
        scr.addstr(": ", output.white)
        scr.addstr(msg, output.white)
