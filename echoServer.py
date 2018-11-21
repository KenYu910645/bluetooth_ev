#!/usr/bin/env python


from bluetooth import *

HOST = ''          # Symbolic name
PORT = 3     # Non-privileged port
s=BluetoothSocket( RFCOMM )

s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()

print 'Connected by', addr
while True:
    data = conn.recv(1024)
    if not data: break
    conn.send(data)
conn.close()
