#!/usr/bin/env python

from bluetooth_template import BLUE_COM
import time 

WAIT_AWK_MAX_TIME = 3 # sec 

blue_com = BLUE_COM()

while blue_com.connect('B8:27:EB:51:BF:F5', 3) == False :
    time.sleep(1)
    print ("[Main] Reconected.")

# blue_com.connect('B8:27:EB:51:BF:F5', 3)

mid = blue_com.send("hello world")
ts = time.time()
while time.time() - ts < wait_awk_max_time: 
    if blue_com.is_awk(mid): # pop out 
        print ("[main] get awk ! send completed (" + mid + ")")
        break
    else:
        time.sleep(0.1)

mid = blue_com.send("hello world")
ts = time.time()
while time.time() - ts < wait_awk_max_time: 
    if blue_com.is_awk(mid): # pop out 
        print ("[main] get awk ! send completed (" + mid + ")")
        break
    else:
        time.sleep(0.1)


print ("[Main] close socket")
blue_com.close() 







