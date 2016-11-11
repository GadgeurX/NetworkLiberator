from threading import Thread
import time
import Packet

class HostMgr(Thread):

    def __init__(self, main):
        Thread.__init__(self)
        self.main = main
        self.hosts = []

    def run(self):
        while True:
            time.sleep(10)
            hosts_data = []
            for host in self.hosts:
                hosts_data.append(host.get_host_data())
            self.main.Client.send(Packet.Packet(1, hosts_data))

    def append_host(self,host):
        self.hosts.append(host)

    def has_host(self, ip):
        for host in self.hosts:
            if host.ip == ip:
                return True
            return False
    
    def diselect_all(self):
        for host in self.hosts:
            host.is_selected = False

    def select_host(self, ip):
        for host in self.hosts:
            if host.ip == ip:
                host.is_selected = True