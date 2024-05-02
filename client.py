import socket
import threading 

FORMAT ="utf-8"
IP = '192.168.10.200'
PORT =5050
HEADER =1024

client  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((IP,PORT))

name = input("type your name:")

def receive():
    while True:
        msg =client.recv(HEADER).decode(FORMAT)
        global name
        if msg=="Name":

            
            client.send(name.encode(FORMAT))
            msg=client.recv(HEADER).decode(FORMAT)
            if msg=="unknown person":
                print("unknown person")
                client.close()
                return
        else:
            print(msg)
def write():
    global name
    while True:
        
        msg = f"{name}: {input('')}"
        client.send(msg.encode(FORMAT))

# print('thread')

rec_thread = threading.Thread(target=receive)
rec_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
