#!/usr/bin/env python
from bluetooth import *

# Create the client socket
client_socket=BluetoothSocket( RFCOMM )

client_socket.connect(("B8:27:EB:51:BF:F5", 3))

client_socket.send("Hello World")

print "Finished"

client_socket.close()
