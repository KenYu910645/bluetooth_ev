#!/usr/bin/env python

from bluetooth_template import BLUE_COM
import time 

WAIT_AWK_MAX_TIME = 3 # sec 

blue_com = BLUE_COM()
while blue_com.connect('B8:27:EB:51:BF:F5', 3) == False :
    time.sleep(1)
    print ("[Main] Reconected.")


mid = blue_com.send("Hello World")
ts = time.time()
while time.time() - ts > WAIT_AWK_MAX_TIME: 
    if blue_com.is_awk(mid): # Pop out 
        print ("[Main] Get Awk ! send completed (" + mid + ")")
        break
    else:
        pass # Not yet

blue_com.close() 





