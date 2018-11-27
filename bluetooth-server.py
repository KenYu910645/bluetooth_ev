#!/usr/bin/env python

from bluetooth_template import BLUE_COM
from global_logger import logger
import threading
import time 
import signal

'''
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
'''

is_running = True
def sigint_handler(signum, frame):
    global is_running
    is_running = False
    logger.warning('[sigint_handler] catched interrupt signal!')
signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

def BT_cmd_CB(msg):
    logger.info("Get msg from main : " + msg) 

blue_com = BLUE_COM(logger, BT_cmd_CB)

blue_com.server_engine_start(port = 3)

while is_running:
    pass 
print ("[Main] server_engine_stop")
blue_com.server_engine_stop()


