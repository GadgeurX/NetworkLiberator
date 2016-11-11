import netifaces
from netaddr import *

for inter in netifaces.interfaces():
    addrs = netifaces.ifaddresses(inter)
    try:
        print(addrs)
        print(addrs[netifaces.AF_INET][0]["addr"])
        print(addrs[netifaces.AF_INET][0]["broadcast"])
        print(addrs[netifaces.AF_INET][0]["netmask"])
        local_ip = addrs[netifaces.AF_INET][0]["addr"]
        broadcast = addrs[netifaces.AF_INET][0]["broadcast"]
        netmask = addrs[netifaces.AF_INET][0]["netmask"]
        gws = netifaces.gateways()
        gateway = gws['default'][netifaces.AF_INET][0]
        interface = inter
        ips = []
        for ip in IPNetwork(broadcast + '/' + str(IPNetwork('0.0.0.0/' + netmask).prefixlen)).iter_hosts():
            ips.append(str(ip))
    except:
        print("Error")

def get_lan_ip():
    global local_ip
    return local_ip

def get_broadcast_ip():
    global broadcast
    return broadcast

def get_all_ips():
    global ips
    return ips

def get_gateway():
    global gateway
    return gateway