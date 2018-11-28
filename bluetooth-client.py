#!/usr/bin/env python

from bluetooth_template import BLUE_COM
from global_logger import logger
import signal 
import threading 
import time 

######################
###  Exit handler  ###
######################
is_running = True
def sigint_handler(signum, frame):
    global is_running
    is_running = False
    logger.warning('[sigint_handler] catched interrupt signal!')
signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

###########################
###  Callback function  ###
###########################
def BT_cmd_CB (msg):
    logger.info("Get msg from BT_cmd_CB : " + msg)


#########################################
###   Config of bluetooth connction   ###
#########################################
blue_com = BLUE_COM(logger, BT_cmd_CB, host = 'B8:27:EB:51:BF:F5', port = 3)
blue_com.client_engine_start()

type_msg = "" 

def input_fun(): 
    global type_msg
    while is_running: 
        type_msg = raw_input('Send:')


###############
###  Loop   ###
###############
input_thread = threading.Thread(target = input_fun)
input_thread.start()
while is_running :
    if type_msg != "":
        blue_com.send(type_msg)
        type_msg = ""

    # Wait 1 sec 
    time.sleep(1)
input_thread.join(1)



#####################
###   End Engine  ###
#####################
print ("[Main] DISCONNECT ")
blue_com.client_engine_stop()







