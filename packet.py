#/usr/bin/python

import time
from socket import socket, AF_INET, SOCK_DGRAM
import struct
import select
import random
import asyncore
import numpy as np

dataseq = 0
helloseq = 0
updateseq= 0
ls = []
ttl = .05


def create_hello(pkttype, seq, ttl, src):
    header = struct.pack('BBBB', pkttype, seq, ttl, src)
    return header

def create_update(pkttype, seq, ttl, src, ls):
    header = struct.pack('BBBB', pkttype, seq, ttl, src)
    return header + ls

def create_data(pkttype, seq, src, kval, dst1, dst2, dst3, nval, kremain, data):
    pktlen = len(data)
    header = struct.pack('BBBBBBBBBB', pkttype, seq, pktlen, src, kval, dst1, dst2, dst3, nval, kremain)
    return header + bytes(data,'utf-8')

def create_dataack(pkttype, seq, src, dest):
    header = struct.pack('BBBB', pkttype, seq, src, dest)
    return header


def read_hello(pkt):
    header = pkt[0:28]
    pkttype, seq, ttl, src = struct.unpack('BBBB', header)
    return pkttype, seq, ttl, src

def read_update(pkt):
    header = pkt[0:28]
    ls = pkt[28:]
    pkttype, seq, ttl, src = struct.unpack('BBBB', header)
    return pkttype, seq, ttl, src, ls

def read_datapacket(pkt):
    header = pkt[0:80]
    pkttype, seq, pktlen, src, kval, dst1, dst2, dst3, nval, kremain = struct.unpack('BBBBBBBBBB', header)
    return pkttype, seq, pktlen, src, kval, dst1, dst2, dst3, nval, kremain

def read_dataack(pkt):
    header = pkt[0:28]
    pkttype, seq, src, dest = struct.unpack('BBBB', header)
    return pkttype, seq, src, dest

def read_data(pkt):
    data = pkt[80:]
    return data

def read_header(pkt):
    pkttype = pkt[0:8]
    return pkttype

def sendhello(h):
    packet = create_hello(0,helloseq, ttl, h.id)
    send_packet(h, packet)
    return 0

def sendupdate(h):
    packet = create_update(1,updateseq, ttl, h.id, ls)
    send_packet(h, packet)
    return 0

def senddata(h, dst1, dst2, dst3, data, k):
    transnum = 0
    packetdata = create_data(2, dataseq, len(data), h.id, k, dst1, dst2, dst3, 3, k, data)
    send_packet(h, packetdata)
    send_time = time.time()

    while (receive_packet(h, packetdata) != -1) & transnum <= 255:
    	transnum+=1
    	send_packet(h, packetdata)
    return 0

def multicast(h, k):
    seq_num = 0
    dataseq = seq_num
    data = 'multicast'
    packet = create_data(2, dataseq, len(data), h.id, k, dst, None, None, 3, k, data)
    send_packet(h, packet)
    send_time = time.time()

def send_packet(h, packet):
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(packet, h.default_gateway)
    s.close()
    print("Sending: ", packet, " To: ", h.default_gateway)
    return 0

def receive_packet(h, sent_packet):
    s = socket(AF_INET, SOCK_DGRAM)
    s.bind((h.ip, h.port))
    seq_failed = -1

    while True:
        try:
            if sent_packet != None:
                s.settimeout(0.05)
            packet,addr = s.recvfrom(1024)
            pkttype, seq, src, dest = read_dataack(packet)
        except OSError:
            pkttype, seq, pktlen, src, kval, dst1, dst2, dst3, nval, kremain = read_datapacket(sent_packet)
            seq_failed = seq
            break
        if(pkttype == 2 and dest == h.id):
            print("Received: ", packet, " From: ", src)
            packet = create_dataack(3, seq, h.id, src)
            send_packet(h, packet)

        elif(pkttype == 3 and dest == h.id):
            break

    s.close()
    return  seq_failed
