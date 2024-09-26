import socket


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "174.6.74.238"
        self.port = 25566
        self.addr = (self.server, self.port)
        self.msg = self.connect()

    def getmsg(self):
        return self.client.recv(2048).decode()

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
        except socket.error as e:
            print(e)