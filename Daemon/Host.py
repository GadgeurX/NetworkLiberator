from threading import Thread
import requests
import json
from scapy.all import *
import Utils

def get_vendor(mac):
    MAC_URL = 'http://macvendors.co/api/%s'
    r = requests.get(MAC_URL % mac).json()
    return r["result"]["company"]

class Host(Thread):

    def __init__(self, ip, mac):
        Thread.__init__(self)
        self.is_selected = False
        self.ip = ip
        self.mac = mac
        self.vendor = "Unknown"
        self.packet = ARP()
        self.packet.timeout = 2.000
        self.packet.op = 2
        self.packet.psrc = Utils.get_gateway()
        self.packet.pdst = ip
        self.packet.hwdst = mac

    def run(self):
        self.vendor = get_vendor(self.mac)

    def get_host_data(self):
        return {"ip":self.ip, "mac":self.mac, "vendor":self.vendor}