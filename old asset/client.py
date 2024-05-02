import socket
import requests,threading
# class client_cls:
#     def __init__(self) -> None:
        
#         self.port = 5050
#         self.server = "192.168.10.23"
#         self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         self.addr = (self.server,self.port)
#         self.client.connect(self.addr)
#         self.HEADER = 64
#         self.FORMAT  = "utf-8"
#         self.disconnect = "disconnect"


#     def send(self,msg):
#         message = msg.encode(self.FORMAT)
#         self.client.send(message)


# cli = client_cls()
# check = input(".....type message...")
# cli.send(check)
# check = input(".....type message...")
# cli.send(check)
# check = input(".....type message...")
# cli.send(check)

HEADER = 1024
FORMAT = 'utf-8'


def write(obj,abc):
    while True:
        try:
            msg =input("type message.....")
            obj.send(msg.encode(FORMAT))
            if msg =="close":
                break
        except:
            obj.close()

def handle_server(obj,abc):
    msg = obj.recv(HEADER).decode(FORMAT)
    print("handle is run")
    if msg=="Name":

        name = input(f'{msg}:')
        obj.send(name.encode(FORMAT))
        msg=obj.recv(HEADER).decode(FORMAT)
        if msg=="unknown person":
            print("unknown person")
    else:
        print(msg)
   
    


def connect_to_private_ip(public_ip, public_port, private_ip, private_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print("public connection is starting")
    client_socket.connect((private_ip, private_port))
    # print("public connection is connected")
    
    request = f"CONNECT {private_ip}:{private_port}"
    # client_socket.send(request.encode())
    thread = threading.Thread(target=handle_server,args=(client_socket,""))
    thread.start()

    thread_write = threading.Thread(target=write,args=(client_socket,""))
    thread_write.start()

    msg = client_socket.recv(HEADER).decode(FORMAT)
    if msg=="Name":

        name = input(f'{msg}:')
        client_socket.send(name.encode(FORMAT))
        msg =client_socket.recv(HEADER).decode(FORMAT)
        if msg=="unknown person":
            print("unknown person")
    else:
        print(msg)
            

    
    
    # write(client_socket)
        

    
    

    
    

# Example usage
# ipaddr = requests.get('http://api.ipify.org').text
public_ip = ''  # Replace with the actual public IP address
public_port = 4400        # Replace with the actual public port
private_ip = '192.168.100.40' # Replace with the actual private IP address
private_port = 5050         # Replace with the actual private port
# print(ipaddr)
connect_to_private_ip(public_ip, public_port, private_ip, private_port)
