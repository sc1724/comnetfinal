from socket import socket, AF_INET, SOCK_DGRAM
from packet import *

#Creates to new server
class udpserver():

        def __init__(self, id, ip, gateway, port):
                self.ip = ip
                self.id = id
                self.default_gateway = gateway
                self.port = port

#Initializes new server and sets it up to receive packets
if __name__ == '__main__':
        print("Server Start...")
        udp_server = udpserver(id=104, ip='192.168.4.1', gateway=('192.168.2.2',8889), port=8878)
        receive_packet(udp_server, None)
