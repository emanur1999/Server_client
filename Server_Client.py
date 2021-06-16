import socket
import threading
import time
import sys
from queue import Queue
from datetime import datetime



NUMBER_OF_THREADS = 3
JOB_NUMBER = [1, 2,3]
queue = Queue()

addresses_connections = []  # global list  collect connection detail about client
flag = True # Node isn't recover yet (reset)


# Create a Socket ( connect two computers)



host = '192.168.56.1' #socket.gethostbyname(socket.gethostname())
port = 9992
print("My IP address "+"| " +host + " |" +" PORT  | " + str(port) + " |")
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM )
s.bind((host, port))
    
# Establish connection with a client (socket must be listening)
# this function listen and accept client connection
def socket_accept():


    s.listen(5)
    
    print("Waiting for connection....")

    while True:    

        conn, address = s.accept()

        s.setblocking(1)  # prevents timeout

        addresses_connections.append([address,conn])
        print("\nNEW CONNECTION:- {} connected.".format(address))

s1=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Act as client 
# try to conntect with any server
def socket_connect():

    while True:

        Host= "192.168.56.7"
        Port = 9993      

        try:
            s1.connect((Host,Port))
            print("Connected with server !")

            break

        except:
            continue


            
 # check whether file receive or not from adjacent node
# If file received then immediately forward to it's adjacent node
def Receive_recovery_file():

    global flag

    while flag:

        check = True
        while check:

            for add_conn in addresses_connections:
                conn = add_conn[1]
                try:
                    msg = conn.recv(1024).decode("utf-8")

                    if msg =='Client':
                        with open("recovery.jpg","wb") as file1:
                            while True:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                file1.write(data)
                            file1.close()
   
                        print("file received succesfully")
                        flag = False    
                        check= False
                        break
                except:
                    pass

            try:
                msg = s1.recv(1024).decode("utf-8")

                if msg =='Server':
                    with open("recovery.jpg","wb") as file1:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            file1.write(data)
                        file1.close()
                    print("file received succesfully")
                    flag = False
                    check= False
            except:
                pass

        # file forward to adjacent node
        forward_recovery_file()    
                      
            
# file forward procedure        
def forward_recovery_file():
    
    # Sending signal msg before sending a file------
    for add_conn in addresses_connections:

        conn = add_conn[1]
        try:
            conn.send(str.encode("Server"))

        except:
            pass    
    try:
        s1.send(str.encode("Client"))

    except:
        pass   
    # Sending Whole file to each node---------

    with  open("recovery.jpg","rb") as file1:
        data = file1.read(1024)
        while data:
            for add_conn in addresses_connections:
                conn = add_conn[1]
                try:
                    conn.send(data)
                except:
                    pass    
            try:
                s1.send(data)
            except:
                pass
            data = file1.read(1024)
        file1.close()

    print("File transfer successfull to adjacent node...")     

    
    
#-------------------------THREADS-------------   
# Create worker threads      

# Do next job that is in the queue (handle connections, send file)

def work():

    while True:

        x = queue.get()

        if x == 1:
            socket_accept()

        if x == 2:
            socket_connect()  

        if x == 3:
            Receive_recovery_file()
        queue.task_done()


def create_workers():

    for _ in range(NUMBER_OF_THREADS):

        t = threading.Thread(target=work)

        t.daemon = True

        t.start()


def create_jobs():

    for x in JOB_NUMBER:

        queue.put(x)

    queue.join()


create_workers()

create_jobs()


