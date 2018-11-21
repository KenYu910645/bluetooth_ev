#!/usr/bin/env python

from bluetooth import *

HOST = ''          # Symbolic name
PORT = 3     # Non-privileged port
s=BluetoothSocket( RFCOMM )

s.bind((HOST, PORT))
s.listen(1)# Server listens to accept 1 connection at a time.

conn, addr = s.accept()

print 'Connected by', addr
while True:
    data = conn.recv(1024)#a maximum of 1024 characters received at a time.
    if not data: break
    conn.send(data)
conn.close()
