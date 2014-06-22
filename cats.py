#!/usr/bin/env/python

import curses, pickle, random

import output
from conversation import Conversation
from host import Host

conversations = {}
files = {}
users = {}
queued = None
commands = {}
gameover = False

def unlockcommand(comm, func=None):
    global commands
    if func == None:
        commands[comm] = globals()[comm]
    else:
        commands[comm] = func

def queueconv(conv):
    global queued
    queued = conv

class InSec(Host):
    def __init__(self):
        Host.__init__(self, "InSec", "65.32.2.133", ["sensenet.log", "a3f15cb.txt", "emplrec0451.log"], ["clientProtector", "sec0451", "SysAdmin"])
        self.state = 1

    def delete(self, f):
        if f == "sensenet.log":
            self.state = 2
            self.removefile("sensenet.log")
            scr = output.scr
            output.openline()
            scr.addstr("WARNING: ", output.red | curses.A_BOLD)
            scr.addstr("Illegal action detected!")
            output.openline()
            conversations["systemname"].run()
            output.openline()
            scr.addstr("Placing linklock on illegal user.")
            self.addfile("fall1ble.lock")
            global gamestate
            gamestate["localhost"].state = 6
            queueconv(conversations["sec1"])
            return True
        return Host.delete(self, f)

    def copy(self, f):
        if f == "a3f15cb.txt":
            return True
        return Host.copy(self, f)

    def fileinfo(self, f):
        if f == "emplrec0451.log":
            output.openline()
            output.scr.addstr("looks like ol' 0451 here was supposed to be at SenseNet earlier.")
            if self.state == 2:
                self.state = 3
        return Host.fileinfo(self,f)

    def filelist(self):
        l = self.files[:]
        l.remove("emplrec0451.log")
        return l

    def disconnect(self):
        if self.state == 2 or self.state == 3:
            error("User is affected by linklock. May not disconnect")
            return False
        elif self.state == 4:
            self.state = 5
            queueconv(conversations["vortex6"])
            global gamestate
            gamestate["localhost"].state = 8
            return True
        return Host.disconnect(self)

    def message(self, u):
        if self.state == 2 and u == "sec0451":
            queueconv(conversations["sec2"])
            return None
        elif self.state == 3 and u == "sec0451":
            queueconv(conversations["sec3"])
            self.state = 4
            return None
        return "Yeah, that sounds extremely stupid"

    def hostinfo(self):
        return "InSec digital Security: With us, your company can feel safe"

    def connect(self):
        scr = output.scr
        output.openline()
        scr.addstr("User: ")
        u = output.getline()
        output.openline()
        scr.addstr("Password: ")
        pw = output.getline("*")
        if self.state > 1 or u != "admin" or pw != "xfz453":
            global gamestate
            if gamestate["localhost"].state == 2:
                gamestate["localhost"].state = 3
            return None
        else:
            return "admin"

class CogDis(Host):
    def __init__(self):
        Host.__init__(self, "CogDis", "112.43.67.2", [], ["greenwitchMean", "v0rt3x", "fortran4evr", "danielCowell", "c4s3"])
        self.state = 0

    def hostinfo(self):
        return "This is the Cognitive Dissidents. Do not distribute this address to people you don't know"

    def connect(self):
        scr = output.scr
        global gamestate
        if gamestate["localhost"].state in range(2, 8):
            error("You have been tempBanned.")
            output.openline()
            scr.addstr("You stay your ass away until you get the trace off your ass - v0rt3x")
            return None
        output.openline()
        scr.addstr("Welcome to ")
        scr.addstr("Cognitive ", output.yellow | curses.A_BOLD)
        scr.addstr("Dissidents", output.red | curses.A_BOLD)
        return "fall1ble"

    def message(self, u):
        if self.state == 0 and u == "v0rt3x":
            self.state = 1
            queueconv(conversations["vortex1"])
            global gamestate
            gamestate["localhost"].state = 2
            return None
        return Host.message(self, u)

    def disconnect(self):
        if self.state == 1:
            self.state = 2
            global gamestate
            gamestate["localhost"].users.append("v0rt3x")
            queueconv(conversations["vortex2"])
            return True
        return Host.disconnect(self)

    def userlist(self):
        output.openline()
        output.scr.addstr("Listing public users only:")
        return Host.userlist(self)


class SenseNet(Host):
    def __init__(self):
        Host.__init__(self, "SenseNet", "243.12.44.8",
            ["access.log", "d4eff2b.txt", "forkbomb.exe", "firstQuarter.doc"], ["WatchDogDaemon", "FenceBuilder", "SysAdmin"])
        self.state = 0
        self.added = False

    def hostinfo(self):
        return "SenseNet global information and entertainment network"

    def userinfo(self, u):
        if u in ["WatchDogDaemon", "FenceBuilder"] and not self.added:
            global gamestate
            gamestate["hosts"].append(InSec())
            self.added = True
        return Host.userinfo(self, u)

    def connect(self):
        if self.state == 0:
            self.state = 1
            queueconv(conversations["onyxsensenet1"])
            unlockcommand("list", lst)
        return "guest"

    def disconnect(self):
        if self.state == 4 and "onyx.lock" not in self.files:
            self.state = 5
            queueconv(conversations["onyxsensenet5"])
            global gamestate
            gamestate["hosts"].append(CogDis())
            unlockcommand("message")
        return True

    def message(self, u):
        return "That is a FANTASTICALLY bad idea."

    def filelist(self):
        if self.state == 1:
            self.state = 2
            queueconv(conversations["onyxsensenet2"])
        elif self.state == 2:
            self.state = 3
            self.removefile("firstQuarter.doc")
            queueconv(conversations["onyxsensenet3"])
            unlockcommand("delete")
        elif self.state == 3:
            self.state = 4
            self.addfile("onyx.lock")
        return Host.filelist(self)

    def delete(self, f):
        if f == "onyx.lock":
            self.removefile("access.log")
            self.removefile("onyx.lock")
            queueconv(conversations["onyxsensenet4"])
            unlockcommand("disconnect")
            return True
        else:
            return Host.delete(self, f)

    def copy(self, f):
        return True

class Localhost(Host):
    def __init__(self):
        Host.__init__(self, "localhost", "127.0.0.1", [], [])
        self.state = 0

    def start(self):
        global conversations
        conversations["onyxstart1"].run() #enable for release
        unlockcommand("info")

    def hostinfo(self):
        if self.state == 0:
            self.state = 1
            unlockcommand("connect")
            queueconv(conversations["onyxstart2"])
            global gamestate
            gamestate["hosts"].append(SenseNet())
        return "Sony Cyberspace 2: 166MHz, 6MB Main Memory"

    def message(self, u):
        if u == "v0rt3x" and self.state == 3:
            self.state = 4
            queueconv(conversations["vortex3"])
            unlockcommand("copy")
            return None
        elif u == "v0rt3x" and self.state == 4 and "d4eff2b.txt" in self.files:
            self.state = 5
            queueconv(conversations["vortex4"])
            unlockcommand("open", opn)
            global gamestate
            gamestate["localhost"].addfile("decrypt.exe")
            return None
        elif u == "v0rt3x" and self.state == 4:
            return "I don't got the data yet"
        elif u == "v0rt3x" and self.state == 6:
            self.state = 7
            queueconv(conversations["vortex5"])
            return None
        return Host.message(self, u)

localhost = Localhost()

gamestate = {
    "localhost": localhost,
    "host": localhost,
    "user": "root",
    "hosts": []
}

def readconvs():
    global conversations
    with open("conversations") as f:
        content = []
        title = None
        for line in f:
            if line == "\n":
                conversations[title] = Conversation(content)
                content = []
            elif line[0] == "#":
                title = line[1:-1]
            elif line[0] == ":":
                content.append((None,line[1:-1]))
            else:
                l = line.split(":")
                content.append((l[0], ":".join(l[1:])[:-1]))

def readfiles():
    global files
    with open("files") as f:
        for line in f:
            s = line.split("#")
            files[s[0]] = "#".join(s[1:])[:-1]

def readusers():
    global users
    with open("users") as f:
        for line in f:
            s = line.split("#")
            users[s[0]] = "#".join(s[1:])[:-1]

def deny(argv, text):
    scr = output.scr
    t = argv[0]
    for arg in argv[1:]:
        t += " " + arg
    sy, sx = scr.getyx()
    for i in range(len(t)):
        scr.delch(sy, sx - i - 1)
        scr.refresh()
        curses.napms(10)

    scr.move(sy, sx - len(t))
    for c in text:
        scr.addch(c)
        scr.refresh()
        curses.napms(30)

    curses.napms(600)
    sy, sx = scr.getyx()

    for i in range(len(text)):
        scr.delch(sy, sx - i - 1)
        scr.refresh()
        curses.napms(10)

    output.removelastline()

def error(text):
    scr = output.scr
    output.openline()
    scr.addstr("Error: ", output.red | curses.A_BOLD)
    scr.addstr(text)

def info(argv):
    global gamestate
    scr = output.scr
    if len(argv) < 2:
        output.openline()
        scr.addstr("Usage: info host|user <name>|file <name>")
    elif argv[1] == "host":
        output.openline()
        scr.addstr(gamestate["host"].hostinfo())
    elif argv[1] == "user":
        if len(argv) < 3:
            error("No user chosen")
        else:
            nfo = False
            found = False
            if argv[2] in gamestate["localhost"].users:
                found = True
                nfo = gamestate["localhost"].userinfo(argv[2])
            if argv[2] in gamestate["host"].users:
                found = True
                nfo = nfo or gamestate["host"].userinfo(argv[2])
            if not found:
                error("User %s not available" % argv[2])
            elif not nfo:
                error("Info for user %s not available" % argv[2])
            else:
                output.openline()
                scr.addstr(users[argv[2]])
    elif argv[1] == "file":
        if len(argv) < 3:
            error("No file chosen")
        else:
            nfo = False
            found = False
            if argv[2] in gamestate["localhost"].files:
                found = True
                nfo = gamestate["localhost"].fileinfo(argv[2])
            if argv[2] in gamestate["host"].files:
                found = True
                nfo = nfo or gamestate["host"].fileinfo(argv[2])
            if not found:
                error("File %s not found" % argv[2])
            elif not nfo:
                error("Info for file %s not available" % argv[2])
            else:
                output.openline()
                scr.addstr(files[argv[2]])
    else:
        error("Cannot display info on %s" % argv[1])
    scr.refresh()

def copy(argv):
    global gamestate
    scr = output.scr
    if gamestate["host"] is gamestate["localhost"]:
        deny(argv, "I'm on my own machine!")
        return
    elif len(argv) < 2:
        error("No file specified")
        return
    elif argv[1] not in gamestate["host"].files:
        error("File not found")
        return

    r = gamestate["host"].copy(argv[1])
    if r == True:
        gamestate["localhost"].addfile(argv[1])
        output.openline()
        scr.addstr("File %s copied" % argv[1])
    elif r == False:
        error("Could not copy file")
    else:
        deny(argv, r)
    scr.refresh()

def delete(argv):
    global gamestate
    scr = output.scr
    if gamestate["host"] is gamestate["localhost"]:
        deny(argv, "Yeah, I got like 300 Megs of Hard Disk Drive, I'm not deleting shit")
    elif len(argv) < 2:
        error("Delete what?")
    elif argv[1] not in gamestate["host"].files:
        error("File %s not found on remote host" % argv[1])
    elif gamestate["host"].delete(argv[1]):
        output.openline()
        scr.addstr("File %s deleted" % argv[1], output.magenta)
    scr.refresh()

def lst(argv):
    global gamestate
    scr = output.scr
    if len(argv) < 2:
        output.openline()
        scr.addstr("Usage: list files|users|hosts")
    elif argv[1] == "files":
        if gamestate["host"] is not gamestate["localhost"]:
            output.openline()
            scr.addstr("Files on remote host %s" % gamestate["host"].name)
            for f in gamestate["host"].filelist():
                output.openline()
                # color?
                scr.addstr(f)
        if len(gamestate["localhost"].files) > 0:
            output.openline()
            scr.addstr("Files on local machine:")
            for f in gamestate["localhost"].filelist():
                output.openline()
                scr.addstr(f)
    elif argv[1] == "users":
        if gamestate["host"] is not gamestate["localhost"]:
            output.openline()
            scr.addstr("Users connected to host %s:" % gamestate["host"].name)
            for u in gamestate["host"].userlist():
                output.openline()
                scr.addstr(u)
        l = gamestate["localhost"].userlist()
        if len(l) > 0:
            output.openline()
            scr.addstr("Also available for messaging:")
            for u in l:
                output.openline()
                scr.addstr(u)
    elif argv[1] == "hosts":
        output.openline()
        scr.addstr("Known hosts:")
        for h in gamestate["hosts"]:
            output.openline()
            scr.addstr("%s (%s)" % (h.address, h.name))
    else:
        error("Cannot list %s" % argv[1])
    scr.refresh()

def exit(argv):
    global gamestate, gameover
    gameover = True

def help(argv):
    global commands
    scr = output.scr
    output.openline()
    scr.addstr("Available commands:")
    for comm in commands:
        output.openline()
        scr.addstr(comm)
    scr.refresh()

def disconnect(argv):
    global gamestate
    scr = output.scr
    if gamestate["host"] is gamestate["localhost"]:
        deny(argv, "Not yet time to jack out...")
        return
    output.openline()
    scr.addstr("Disconnecting from %s" % gamestate["host"].name)
    if gamestate["host"].disconnect():
        gamestate["host"] = gamestate["localhost"]
        gamestate["user"] = "root"
        scr.refresh()
        return True
    else:
        error("Could not disconnect")
        scr.refresh()
        return False

def message(argv):
    global gamestate
    scr = output.scr
    if len(argv) < 2:
        output.openline()
        scr.addstr("Usage: message <user>")
    elif argv[1] not in gamestate["host"].users + gamestate["localhost"].users:
        error("User %s not available" % argv[1])
    else:
        m = None
        if argv[1] in gamestate["host"].users:
            m = gamestate["host"].message(argv[1])
        else:
            m = gamestate["localhost"].message(argv[1])
        if m != None:
            deny(argv, m)
    scr.refresh()

def connect(argv):
    global gamestate
    scr = output.scr
    if len(argv) < 2:
        error("Connect to what?")
        return
    elif argv[1].lower() == "localhost" or argv[1] == "127.0.0.1":
        deny(argv, "That's my machine, I don't need to connect to that")
        return
    elif argv[1] == gamestate["host"].name or argv[1] == gamestate["host"].address:
        deny(argv, "I'm already connected to those guys")
        return
    targets = [x for x in gamestate["hosts"] if x.name.lower() == argv[1].lower() or x.address == argv[1]]
    if gamestate["host"] is gamestate["localhost"] or disconnect([]):
        output.openline()
        scr.addstr("Connecting to %s" % argv[1])
        scr.refresh()
        curses.napms(1500)
        if len(targets) == 0:
            scr.addstr(", could not be resolved", output.magenta)
            error("Could not connect to %s" % argv[1])
            scr.refresh()
            return
        scr.addstr(", resolved to %s" % targets[0].address)
        scr.refresh()
        curses.napms(500)
        output.openline()
        scr.addstr("Connected.")
        scr.refresh()
        curses.napms(500)
        u = targets[0].connect()
        if u != None:
            gamestate["host"] = targets[0]
            gamestate["user"] = u
        else:
            error("Connection refused by %s" % targets[0].name)
    scr.refresh()

def opn(argv):
    global gamestate
    scr = output.scr
    if len(argv) < 2:
        error("Open what?")
    elif argv[1] not in gamestate["localhost"].files:
        if argv[1] in gamestate["host"].files:
            error("Can only open locally saved files. copy first")
        else:
            error("File %s not found" % argv[1])
    elif gamestate["localhost"].fileinfo(argv[1]):
        if argv[1] == "decrypt.exe":
            output.openline()
            scr.addstr("Installing decrypt utility.")
            scr.refresh()
            curses.napms(1000)
            scr.addstr(".")
            scr.refresh()
            curses.napms(1000)
            scr.addstr(".")
            scr.refresh()
            curses.napms(1000)
            scr.addstr("Success")
            unlockcommand("decrypt")
            gamestate["localhost"].files.remove("decrypt.exe")
        elif argv[1] == "forkbomb.exe":
            for i in range(output.lines * output.cols):
                x = random.randint(0, output.cols -1)
                y = random.randint(0, output.lines -1)
                c = random.randint(32, 126)
                scr.addch(y, x, c)
                scr.refresh()
                curses.napms(1)
            curses.napms(2000)
            global gameover
            gameover = True
        else:
            output.openline()
            scr.addstr(files[argv[1]])
    else:
        error("File not available")
    scr.refresh()

def decr(f, f2):
    global gamesate
    gamestate["localhost"].files.remove(f)
    scr = output.scr
    output.openline()
    scr.addstr("Decrypting %s:" % f)
    output.openline()
    scr.addstr("[" + 30 * " " + "]")
    output.lastline()
    scr.addstr("[")
    scr.refresh()
    for i in range(30):
        curses.napms(100)
        scr.addstr("#")
        scr.refresh()
    output.openline()
    scr.addstr("File %s was decrypted successfully. Result saved in %s" % (f, f2))
    gamestate["localhost"].addfile(f2)

def decrypt(argv):
    global gamestate
    scr = output.scr
    if len(argv) < 2:
        error("Decrypt what?")
    elif argv[1] not in gamestate["localhost"].files:
        if argv[1] in gamestate["host"].files:
            error("Can only decrypt locally saved files. copy first")
        else:
            error("File %s not found" % argv[1])
    else:
        if argv[1] == "d4eff2b.txt":
            decr(argv[1], "inSecPW.txt")
        elif argv[1] == "a3f15cb.txt":
            decr(argv[1], "employeeRecords.txt")
        else:
            error("Could not decrypt file %s." % argv[1])
    scr.refresh()

def prompt():
    global gamestate
    scr = output.scr
    attrs = output.magenta
    if gamestate["user"] == "root":
        attrs |= curses.A_BOLD
    output.openline()
    scr.addstr(gamestate["user"], attrs)
    scr.addstr("@")
    scr.addstr(gamestate["host"].address, output.cyan)
    scr.addstr("> ")
    scr.refresh()

def save(argv):
    global gamestate, commands
    with open("savegame", "wb") as f:
        pickle.dump([gamestate, list(commands.keys())], f, 0)
    output.openline()
    output.scr.addstr("Game saved.")
    scr.refresh()

def load(argv):
    global gamestate
    l = None
    try:
        with open("savegame", "rb") as f:
            l = pickle.load(f)
    except IOError:
        output.scr.addstr("Couldn't load savegame.")
        return
    gamestate = l[0]
    for comm in l[1]:
        if comm == "list":
            unlockcommand(comm, lst)
        elif comm == "open":
            unlockcommand(comm, opn)
        else:
            unlockcommand(comm)
    output.clearscreen()
    output.scr.addstr("Game loaded.")
    scr.refresh()

if __name__ == "__main__":
    readconvs()
    readfiles()
    readusers()
    output.init()
    try:
        scr = output.scr
        curses.napms(1000)
        localhost.start()
        unlockcommand("exit")
        unlockcommand("help")
        unlockcommand("save")
        unlockcommand("load")
        while not gameover:
            prompt()
            line = output.getline()
            argv = line.split(" ")
            if argv[0] in commands:
                commands[argv[0]](argv)
            elif argv[0] in ["fuck", "shit", "asshole"]:
                deny(argv, "Ain't no proper language for a lady!")
            elif argv[0] != "":
                error("Unknown command %s" % argv[0])
            if queued != None:
                output.openline()
                queued.run()
                queued = None

    except KeyboardInterrupt:
        pass
    output.uninit()


