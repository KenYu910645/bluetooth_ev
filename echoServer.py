#!/usr/bin/env python
import sys
from bluetooth import *

HOST = sys.argv[1]       # The remote host
PORT = 8888                 # Server port

s=BluetoothSocket( RFCOMM )

s.connect((HOST, PORT))

while True :
   message = raw_input('Send:')
   if not message : break
   s.send(message)
   data = s.recv(1024)
   print 'Received', `data`
s.close()
