
import sys
import socks
#import socket

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor

print('STARTING PROVA')

#s = socks.socksocket()
#s.set_proxy(socks.SOCKS5, 'gateway', 9050)
def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
#s.getaddrinfo = getaddrinfo


class Prova(Protocol):

    def connectionMade(self):
        print("conn made")
        sys.stdout.flush()
        self.socket = socks.socksocket()
        self.socket.set_proxy(socks.SOCKS5, 'gateway', 9050)
        self.socket.getaddrinfo = getaddrinfo
        self.socket.connect(('msydqstlz2kzerdg.onion', 80))
        print("connected to ahmia")
        sys.stdout.flush()

    def connectionLost(self, reason):
        print("conn lost")
        sys.stdout.flush()
        if self.socket:
            self.socket.close()


    def dataReceived(self, data):
        print("data recieved")
        sys.stdout.flush()
        self.socket.sendall(data)
        print("data sent")
        sys.stdout.flush()
        data = self.socket.recv(1024)
        while data:
            self.transport.write(data)
            data = self.socket.recv(1024)
        self.transport.loseConnection()
        print("loosin connection")
        sys.stdout.flush()


class ProvaFactory(Factory):

    def buildProtocol(self, addr):
        return Prova()

print('STARTING REACTOR')
sys.stdout.flush()
reactor.listenTCP(8000, ProvaFactory())
reactor.run()
