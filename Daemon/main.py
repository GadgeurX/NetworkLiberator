#!/usr/bin/env python3
import os, sys, signal
euid = os.geteuid()
if euid != 0:
    print("Script not started as root. Running sudo..")
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)
print('Running. Your euid is', euid)
sys.path.insert(0, './Network')
from NetworkMgr import Client
from ArpDetector import ArpDetector
from HostMgr import HostMgr
from NetworkScanner import NetworkScanner
from AttackProcess import AttackProcess
import nmap

class Main():

    def __init__(self):
        
        self.nm = nmap.PortScanner()
        self.HostMgr = HostMgr(self)
        self.HostMgr.start()

        self.ArpDetector = ArpDetector(self)
        self.ArpDetector.start()

        self.Client = Client(self)
        self.Client.start()

        self.NetworkScanner = NetworkScanner(self)
        self.NetworkScanner.start()

        self.AttackProcess = AttackProcess(self)
        self.AttackProcess.start()

signal.signal(signal.SIGINT, signal.SIG_DFL)
main = Main()