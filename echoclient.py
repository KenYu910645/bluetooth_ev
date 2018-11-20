import sys
import time
from bluetooth import *
import bluetooth

# HOST = sys.argv[1]       # The remote host
HOST = '10:02:B5:D4:1C:3B'
PORT = 3                 # Server port

# s.connect((HOST, PORT))

count = 0
while True :
   try:
      s=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
      s.connect((HOST, PORT))
   except:
      print "reconnect"
      continue
   # message = raw_input('Send:')
   message = str(count)
   if not message : break

   try:
      s.send(message)
      data = s.recv(1024)
   except:
      print "reconnect"
      continue
   print 'Received', `data`
   count = count + 1

   s.close()
   time.sleep(1)
#s.close()
