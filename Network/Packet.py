import pickle

class Packet():

    def __init__(self, id, data):
        self.id = id
        self.data = data

def get_pickled_packet(packet):
    return pickle.dumps(packet)

def get_unpickled_packet(packet):
    return pickle.loads(packet)