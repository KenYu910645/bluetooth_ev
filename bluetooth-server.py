#!/usr/bin/env python

from bluetooth_template import BLUE_COM
from global_logger import logger
import threading
import time 
import signal

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
def BT_cmd_CB(msg):
    logger.info("Get msg from main : " + msg) 


#########################################
###   Config of bluetooth connction   ###
#########################################
blue_com = BLUE_COM(logger, BT_cmd_CB, host = None , port = 3 )

############################################
###   Start server engine at background  ###
############################################
blue_com.server_engine_start()


###############
###  Loop   ###
###############
while is_running:
    time.sleep(1)
print ("[Main] server_engine_stop")

#####################
###   End Engine  ###
#####################
blue_com.server_engine_stop()


