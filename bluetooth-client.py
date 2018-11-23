#!/usr/bin/env python

from bluetooth_template import BLUE_COM
from global_logger import logger
import signal 
import time 

is_running = True
def sigint_handler(signum, frame):
    global is_running
    is_running = False
    print('[sigint_handler] catched interrupt signal!')
signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGHUP, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)

WAIT_AWK_MAX_TIME = 20 # sec 

blue_com = BLUE_COM(logger)

while blue_com.connect('B8:27:EB:51:BF:F5', 3) == False and is_running :
    time.sleep(1)
    print ("[Main] Reconected.")

# blue_com.connect('B8:27:EB:51:BF:F5', 3)

while is_running: 
    sa = blue_com.send("hello world")
    ts = time.time()
    while time.time() - ts < WAIT_AWK_MAX_TIME: 
        if sa.is_awk : # pop out 
            break
        else:
            time.sleep(0.1)
    time.sleep (1)

print ("[Main] close socket")
blue_com.close() 







