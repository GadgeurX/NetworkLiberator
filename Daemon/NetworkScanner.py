from threading import Thread
import Utils
from scapy.all import *
import os
import sys
from Host import Host

def get_mac(ip_address, timeout, retry):
    responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address), timeout=timeout, retry=retry)
    for s,r in responses:
        return r[Ether].src
    return None

class NetworkScanner(Thread):

    def __init__(self, main):
        Thread.__init__(self)
        self.main = main

    def run(self):
        self.scan(0.020, 2)
        print(self.main.HostMgr.hosts)
        while True:
            self.scan(2, 2)

    def scan(self, timeout, retry):
        for ip in Utils.get_all_ips():
            if not self.main.HostMgr.has_host(ip):
                mac = get_mac(ip, timeout, retry)
                if mac is not None:
                    host = Host(self.main, ip, mac)
                    host.start()
                    self.main.HostMgr.append_host(host)