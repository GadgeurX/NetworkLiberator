import os, time, sys, Utils
from sys import platform
from scapy.all import sniff
import Packet
from threading import Thread
import threading

request_threshold = 3
requests = []
replies_count = {}


class ArpDetector(Thread):

    def __init__(self, main):
        Thread.__init__(self)
        self.main = main
        print(Utils.get_all_ips())
        print("Initialize ArpDetector")

    def run(self):
        self.run = True
        self.reset_reply_count()
        sniff(filter = "arp", prn = self.packet_filter, store = 0)

    def reset_reply_count(self):
        global replies_count
        print("Reset detector reply")
        for reply in replies_count:
            replies_count[reply] = 0
        threading.Timer(60, self.reset_reply_count).start()
        
    def check_spoof (self, source, mac, destination):
        global request_threshold, requests, replies_count, notification_issued
        if destination == Utils.get_broadcast_ip():
            if not mac in replies_count:
                replies_count[mac] = 0

        if not source in requests and source != Utils.get_lan_ip():
            if not mac in replies_count:
                replies_count[mac] = 0
            else:
                replies_count[mac] += 1

            if (replies_count[mac] > request_threshold):
                print("attack")
                replies_count[mac] = -50
                self.issue_os_notification("ARP Spoofing Detected", "ARP Spoofing Attack Detected from {}.".format(mac))
        else:
            if source in requests:
                requests.remove(source)

    def packet_filter(self, packet):
        global requests
        source = packet.sprintf("%ARP.psrc%")
        dest = packet.sprintf("%ARP.pdst%")
        source_mac = packet.sprintf("%ARP.hwsrc%")
        operation = packet.sprintf("%ARP.op%")
        if source == Utils.get_lan_ip():
            requests.append(dest)
        if operation == 'is-at':
            return self.check_spoof(source, source_mac, dest)

    def issue_os_notification(self,title, content):
            self.main.Client.send(Packet.Packet(0, {"title":title, "content":content}))

    def stop(self):
        self.run = False
        print("Stop ARP Detector...")