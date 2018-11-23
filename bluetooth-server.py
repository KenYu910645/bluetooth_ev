#!/usr/bin/env python

from bluetooth_template import BLUE_COM
import threading
import time 

'''
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
'''

blue_com = BLUE_COM()

blue_com.server_engine_start(port = 3)

#server_sock.close()
#print("[main] BlueTooth server end")
