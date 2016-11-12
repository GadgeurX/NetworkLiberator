from threading import Thread
import time
from scapy.all import *


class AttackProcess(Thread):

    def __init__(self, main):
        Thread.__init__(self)
        self.main = main
        self.selected_hosts = []
        self.is_attacking = False

    def run(self):
        while True:
            while self.is_attacking:
                packets = []
                for host in self.main.HostMgr.hosts:
                    if host.is_selected:
                        packets.append(host.packet)
                time.sleep(1)
                send(packets)
            time.sleep(5)