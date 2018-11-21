#!/usr/bin/env python
import sys
from bluetooth import *

# HOST = str(sys.argv[1])       # The remote host
PORT = 8888                 # Server port

s=BluetoothSocket( RFCOMM )
#print "HOST: ", HOST
s.connect(("B8:27:EB:51:BF:F5", 3))

print "After"
while True :
   message = raw_input('Send:')
   if not message : break
   s.send(message)
   data = s.recv(1024)
   print 'Received', `data`
s.close()
