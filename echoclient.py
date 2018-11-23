#!/usr/bin/env python
import sys
from bluetooth import *

import time 
# HOST = str(sys.argv[1])       # The remote host
PORT = 8888                 # Server port

s=BluetoothSocket( RFCOMM )
#print "HOST: ", HOST
s.connect(("B8:27:EB:51:BF:F5", 3))

s.settimeout(1)
while True :
   # message = raw_input('Send:')
   message = "test"
   s.send(message)
   print ("Send message")
   print ("Before recv") 
   try:  
      data = s.recv(1024)
   except: 
      print ("except")
   else: 
      print ("After recv")  
      print 'Received', `data`
   time.sleep(1)
s.close()
