#!/usr/bin/python3

import sys
import socket

argsString = ';'.join(sys.argv) # prepare to pass args to server

def client():
    # connect to server
    host = socket.gethostname()
    port = 8181
    s = socket.socket()
    s.connect((host, port))

    # pass args to server
    s.send(argsString.encode('utf-8'))
    # get and print device status response
    lightResponse = s.recv(1024).decode('utf-8')
    print(lightResponse)
    #close connection to server
    s.close()

client()