#!/usr/bin/env python

from bluetooth_template import BLUE_COM
from global_logger import logger
import signal 
import threading 
import time 

is_running = True
def sigint_handler(signum, frame):
    global is_running
    is_running = False
    logger.warning('[sigint_handler] catched interrupt signal!')
signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

WAIT_AWK_MAX_TIME = 20 # sec 

def BT_cmd_CB (msg):
    logger.info("Get msg from BT_cmd_CB : " + msg)
    

blue_com = BLUE_COM(logger, BT_cmd_CB)
blue_com.client_engine_start()
# blue_com.connect('B8:27:EB:51:BF:F5', 3)

type_msg = "" 

def input_fun(): 
    global type_msg
    while is_running: 
        type_msg = raw_input('Send:')

input_thread = threading.Thread(target = input_fun)# , args=(self.sock,))  # (self.sock))
input_thread.start()
while is_running :
    if type_msg != "":
        blue_com.send(type_msg)
        type_msg = ""

    # Wait 1 sec 
    time.sleep(1)
print ("Before")
input_thread.join(5)
print ("After ")
'''
while is_running: 
    if blue_com.is_connect: 
        
        sa = blue_com.send("hello world")
        ts = time.time()
        while time.time() - ts < WAIT_AWK_MAX_TIME: 
            if sa.is_awk : # pop out 
                break
            else:
                time.sleep(0.1)
        
        
    else: 
        logger.info("[Main] Reconnected.")
        blue_com.connect('B8:27:EB:51:BF:F5', 3)
    time.sleep(1)
'''

print ("[Main] DISCONNECT ")
blue_com.client_engine_stop()







