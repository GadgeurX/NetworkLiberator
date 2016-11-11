#!/usr/bin/env python3

import os, sys, signal
import sys
sys.path.insert(0, './Network')
from NetworkMgr import Server
from AppIndicator import AppIndicator
from AttackWindow import AttackWindow

class Main():

    def __init__(self):

        self.AttackWindow = AttackWindow(self)

        self.AppIndicator = AppIndicator(self)
        self.AppIndicator.start()

        self.Server = Server(self)
        self.Server.start()
        os.system("./Daemon/main.py")

signal.signal(signal.SIGINT, signal.SIG_DFL)
main = Main()