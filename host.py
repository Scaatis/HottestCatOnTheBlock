#!/usr/bin/env python

import curses, output

class Host:
    def __init__(self, name, address, files=[], users=[]):
        self.name = name
        self.address = address
        self.files = sorted(files)
        self.users = sorted(users)

    def connect(self):
        return "guest"

    def disconnect(self):
        return True

    def filelist(self):
        return self.files

    def userlist(self):
        return self.users

    def copy(self, f):
        return "I don't want that"

    def delete(self, f):
        output.openline()
        scr = output.scr
        scr.addstr("Access Denied")
        return False

    def upload(self, f):
        addfile(f)
        return True

    def hostinfo(self):
        return "No info available"

    def userinfo(self, user):
        return True

    def fileinfo(self, file):
        return True

    def message(self, user):
        return "Don't wanna talk to them"

    def addfile(self, f):
        self.files.append(f)
        self.files.sort()

    def removefile(self, f):
        self.files.remove(f)


