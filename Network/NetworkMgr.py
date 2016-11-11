import socket
import select
import Packet
import PacketProcess
from threading import Thread

class Server(Thread):

    def __init__(self, main):
        Thread.__init__(self)
        print("Initialize Server")
        self.main = main
        self.SSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.SSocket.bind(('127.0.0.1',8820))
        self.SSocket.listen(1)
        self.clients = []
        self.queue = []
        self.data = b""

    def run(self):
        run = True
        while run:
            requests, wlist, xlist = select.select([self.SSocket],[], [], 0.05)
            for request in requests:
                print("New Connection")
                CSocket, infos_connexion = request.accept()
                self.clients.append(CSocket)

            PSockets = []
            try:
                PSockets, wlist, xlist = select.select(self.clients,[], [], 0.05)
            except select.error:
                pass
            else:
                for CSocket in PSockets:
                    pdata = CSocket.recv(1024)
                    PPacket = self.process_data(pdata)
                    if PPacket is not None:
                        print(PPacket)
                        packet = Packet.get_unpickled_packet(PPacket)
                        PacketProcess.process_packet(packet, self.main)
            while len(self.queue) > 0:
                self.clients[0].send(Packet.get_pickled_packet(self.queue[0]))
                self.clients[0].send(b"bite")
                del self.queue[0]

    def process_data(self, pdata):
        self.data += pdata
        if self.data.find(b"bite") is not -1:
            result = self.data.split(b"bite", 1)
            if len(result) > 1:
                self.data = result[1]
            return result[0]
        return None

    def send(self, packet):
        self.queue.append(packet)

class Client(Thread):

    def __init__(self, main):
        Thread.__init__(self)
        self.main = main
        print("Initialize Client")
        self.CSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CSocket.connect(("127.0.0.1", 8820))
        self.queue = []
        self.data = b""

    def run(self):
        print("Start Client")
        run = True
        while run:

            PSockets = []
            try:
                PSockets, wlist, xlist = select.select([self.CSocket],[], [], 0.05)
            except select.error:
                pass
            else:
                for sock in PSockets:
                    pdata = sock.recv(1024)
                    SPacket = self.process_data(pdata)
                    if SPacket is not None:
                        packet = Packet.get_unpickled_packet(SPacket)
                        PacketProcess.process_packet(packet, self.main)
            while len(self.queue) > 0:
                self.CSocket.send(Packet.get_pickled_packet(self.queue[0]))
                self.CSocket.send(b"bite")
                del self.queue[0]

    def process_data(self, pdata):
        self.data += pdata
        if self.data.find(b"bite") is not -1:
            result = self.data.split(b"bite", 1)
            if len(result) > 1:
                self.data = result[1]
            return result[0]
        return None

    def send(self, packet):
        self.queue.append(packet)