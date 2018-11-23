#!/usr/bin/env python
# file: rfcomm-client.py
# auth: Albert Huang <albert@csail.mit.edu>
# desc: simple demonstration of a client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
#
# $Id: rfcomm-client.py 424 2006-08-24 03:35:54Z albert $

from bluetooth import *
import sys
import time
import random # for getMid()
import threading

REC_TIMEOUT = 0.1 # Sec 
START_CHAR = '['
END_CHAR = ']'

class BLUE_COM(): # PING PONG TODO 
    def __init__(self):
        # -------- Connection --------# 
        self.is_connect = False
        self.sock = None 
        self.recv_thread = None 
        self.is_server_engine_running = False  
        #-------- For Recevied -------# 
        # self.recbufArr = []
        self.recbufDir = dict() # key: "MID"  , value ,payload  # TODO infinitly expand 
        # self.tid_counter = 0
    
    def server_engine_start(self, port = 3): # Totolly blocking function 
        self.sock=BluetoothSocket(RFCOMM)
        self.sock.bind(("",port))
        self.sock.listen(1)

        self.is_server_engine_running = True 
        self.server_thread = threading.Thread(target = self.server_engine, args=(port,))
        self.server_thread.start()

    def server_engine_stop(self):
        try:
            self.is_connect = False 
            self.is_server_engine_running = False 
            self.server_thread.join()
            self.recv_thread.join()
            self.sock.close() # Server socket close 
            print("[server_engine_stop] BlueTooth server end")
        except : 
            print("[server_engine_stop] Fail to close socket or server engine.")

    def server_engine (self, port): # ToTally Blocking 
        #client_sock.settimeout(1)               
        # try:
        if True : 
            while self.is_server_engine_running: # Durable Server
                #---------
                print("[server_engine] Waiting for connection on RFCOMM channel %d" % port)
                client_sock, client_info = self.sock.accept() # Blocking 
                print("[server_engine] Accepted connection from "+  str(client_info))
                self.is_connect = True 
                # TODO 
                
                self.recv_thread = threading.Thread(target = self.recv_engine, args=(client_sock,))
                self.recv_thread.start()

                while self.is_connect:
                    time.sleep(1) 

                print ("[server_engine] Disconnection from " + str(client_info) + "Stop recv thread.")
                self.recv_thread.join()
        # except IOError:
        # xcept: 
        else: 
            print ("[server_engine] Something wrong at server_engine.")

            # print ("IOERROR!!!")
            # print("[main] disconnected from " + str(client_info))
        
        # client_sock.close()

    def connect (self, host = 'B8:27:EB:51:BF:F5', port = 3):
        print("[BlueTooth] connecting to " + host)
        ts = time.time()
        # Create the client socket
        self.sock=BluetoothSocket(RFCOMM)
        try: 
            self.sock.connect((host, port)) # What if can't connected TODO
        except: 
            print ("[BlueTooth] Not able to Connect")
            rc = False 
        else : 
            rc = True 
            self.is_connect = True 
            print("[BlueTooth] connected. Spend " + str(time.time() - ts) + " sec.") #Link directly, Faster ????? TODO 

            self.recv_thread = threading.Thread(target = self.recv_engine, args=(self.sock,))  # (self.sock))
            self.recv_thread.start()
            
        return rc 

    def close(self): 
        # if self.sock != None:
        try: 
            self.is_connect = False 
            if self.recv_thread.is_alive():
                print ("[close] waiting join recv_threading ")
                self.recv_thread.join()
                # print ("[close] waiting join recv_threading ")
            print ("Close socket")
            self.sock.close() 
            self.sock = None 
        # else: 
        except : 
            print ("[close] Can't close.")
    
    def getMid(self):
        '''
        return A(65)~Z(90) in sequence
        '''
        # global tid_counter
        #output = chr(65 + (tid_counter/26)) + chr(65 + tid_counter%26) # AA, AB, AC
        # output = chr(65 + self.tid_counter)
        # output = str(self.tid_counter)
        output = "" 
        for i in range(4) : 
            output += chr(random.randint(1,26) + 65)
        return output

    def send (self, payload):
        '''
        Inptu : payload need to be STring
        Definetly nonblocking send.
        return mid 
        '''
        print ("[send] Sending: " + payload) # totally non-blocking even if disconnect
        mid = self.getMid()
        self.sock.send( '['+payload+',mid'+ mid+']')
        return mid
    
    def is_awk (self, mid):
        '''
        Input : Mid ('SDFR', "TYHG")
        Output : True (Get AWK), False (Not yet ) 
        '''
        ans = self.recbufDir.pop(mid, "not match") # Pop out element, if exitence 

        if ans != "not match": # Get something 
            if ans == 'awk':
                return True 
            else:
                print ('[is_send_awk] mid is found, but content is not AWK.')
                return False
        else: 
            # print ('[is_send_awk] MID NOT FOUND ')
            return False 

    def recv_engine(self, recv_sock): # Totolly -blocking  TODO  # Only block when something is need to recv , MAX BLOCK time is REC_TIMEOUT
        recv_sock.settimeout(1)
        while self.is_connect:
            try: 
                rec = recv_sock.recv(1024) # Blocking for 1 sec. 
                print (rec)
            except : 
                print ("[recv_engine] timeout ")
                continue 
                # logger.error("[EVwaitAnswer] read fail")
            else: 
                try:
                    mid_str = rec[-8:]# ,midASDF
                    rec = rec[:-8] # Cut off mid 
                    #---------  Check MID --------# 
                    if mid_str[:4] != ',mid' or (not mid_str[4:].isupper()):
                        is_valid = False 
                    else: 
                        is_valid = True 
                except: 
                    is_valid = False 
                    print ("[recv_engine] MID ERROR ")

                if is_valid: 
                    # self.recbufArr.append(rec)
                    self.recbufDir[mid_str[4:]] = rec
                    if rec != "awk":
                        print ("Sending AWK")
                        recv_sock.send( '[awk,mid'+mid_str[4:]+']') # Send AWK to back to sender 
                else: 
                    print ("[recv_engine] Not Valid ")
                # ------ Reset Flag --------# 
                rec = ""
    '''
    def recv_engine (self, recv_sock): # Totolly -blocking  TODO  # Only block when something is need to recv , MAX BLOCK time is REC_TIMEOUT
        recv_sock.settimeout(1)
        rec_state = "waiting"
        rec = ""
        recbuf = ""
        while self.is_connect : 
            try: 
                rec = recv_sock.recv(1)# Non blocking # TODO Check for blocking
                print (rec)
            except:
                print ("[recv_engine] read fail")
                time.sleep(0.1)
                continue 
                # logger.error("[EVwaitAnswer] read fail")
            else: 
                pass 

            # -------- State Machine --------#
            # tStartWait = time.time()
            # if rec_state == "receiving": # time.time() - tStartWait < REC_TIMEOUT: # ~= 0.1 sec
                # if device.inWaiting() != 0: # Wait for ST_board answer, Should be '[H]' or '[L]'
                #----- Timeout Check -------# 
                #if time.time() - tStartWait < REC_TIMEOUT:
                #    rec_state = "timeout"
                #------ RECVEIVED--------# 
            if rec_state == "waiting":
                if rec == START_CHAR : 
                    rec_state = "receiving"
                else: 
                    print ("[Trash] rec ")
            elif rec_state == "receiving":
                if rec == END_CHAR:# is_completed
                    # rec_state = "waiting"
                    rec_state = "completed"
                elif rec == START_CHAR:
                    recbuf = ""
                else:
                    recbuf += rec
            
            
            if rec_state == "completed":
                print ("COmpleted recbuf: " + str(recbuf))
                #self.is_valid = True 
                #if self.is_valid:
                # Check mid ??!!
                try:
                    mid_str = recbuf[-8:]# ,midASDF
                    recbuf = recbuf[:-8] # Cut off mid 
                    #---------  Check MID --------# 
                    if mid_str[:4] != ',mid' or (not mid_str[4:].isupper()):
                        is_valid = False 
                    else: 
                        is_valid = True 
                except: 
                    is_valid = False 
                    print ("[recv_engine] MID ERROR ")

                if is_valid: 
                    # self.recbufArr.append(recbuf)
                    self.recbufDir[mid_str[4:]] = recbuf
                    if recbuf != "awk":
                        print ("Sending AWK")
                        recv_sock.send( '[awk,mid'+mid_str[4:]+']') # Send AWK to back to sender 
                else: 
                    print ("[recv_engine] Not Valid ")
                
                # ------ Reset Flag --------# 
                recbuf = ""
                rec_state = "waiting"
            #elif rec_state == "timeout":
            #    print ("[recv_engine] TIMEOUT !! ")
 
                
                # time.sleep(0.001) #TODO test#sleep 1ms, check device for every 1ms
                # End of receiving while
            # End of Engine while 
            time.sleep(0.001) #TODO test#sleep 1ms, check device for every 1ms 
    '''
