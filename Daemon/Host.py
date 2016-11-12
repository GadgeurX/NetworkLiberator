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

    def __init__(self,main, ip, mac):
        Thread.__init__(self)
        self.main = main
        self.is_selected = False
        self.ip = ip
        self.mac = mac
        self.vendor = "Unknown"
        self.os = "Unknown"

        self.packet = ARP()
        self.packet.timeout = 2.000
        self.packet.op = 2
        self.packet.psrc = Utils.get_gateway()
        self.packet.pdst = ip
        self.packet.hwdst = mac

    def run(self):
        self.vendor = get_vendor(self.mac)
        self.os = self.get_os(self.ip)

    def get_host_data(self):
        return {"ip":self.ip, "mac":self.mac, "vendor":self.vendor, "os":self.os}

    def get_os(self, ip):
        self.main.nm.scan(ip, arguments="-O")
        if 'osclass' in self.main.nm[ip]:
            for osclass in self.main.nm[ip]['osclass']:
                print("********************************************************************************")
                print('OsClass.type : {0}'.format(osclass['type']))
                print('OsClass.vendor : {0}'.format(osclass['vendor']))
                print('OsClass.osfamily : {0}'.format(osclass['osfamily']))
                print('OsClass.osgen : {0}'.format(osclass['osgen']))
                print('OsClass.accuracy : {0}'.format(osclass['accuracy']))
                print("********************************************************************************")
                print('')

        if 'osmatch' in self.main.nm[ip]:
            for osmatch in self.main.nm[ip]['osmatch']:
                return osmatch['name']

        if 'fingerprint' in self.main.nm[ip]:
            print("********************************************************************************")
            print('Fingerprint : {0}'.format(self.main.nm[ip]['fingerprint']))
            print("********************************************************************************")
        return "Unknown"