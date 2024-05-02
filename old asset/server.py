import requests
import socket
import threading
# ipaddr = requests.get('http://api.ipify.org').text

IP= socket.gethostbyname(socket.gethostname())
print(IP)
PORT= 5050
HEADER = 1024
FORMAT = 'utf-8'
# print(ipaddr)


class users:
    def __init__(self) -> None:
        self.users_lst = {}

    def add_users(self,name:str):
        self.users_lst[name]=[]

    def remove_users(self,name):
        del self.users_lst[name]
        # self.users_lst.remove(index)

    def check_user(self,name):
        if name in self.users_lst:
            return True
        return False
    def add_conn_obj(self,name,obj):
        self.users_lst[name].append(obj)

        
user = users()
user.add_users("hassam")
user.add_users("haider")

def broadcast(msg,name):
    for i in user.users_lst:
        print("broadcast")
        if user.users_lst[i]:
            print("user object")
            user.users_lst[i][0].send(f"{name}:{msg}".encode(FORMAT))


def handle_client(socket_obj,ret_addr,name):
    try:
        msg = socket_obj.recv(HEADER).decode(FORMAT)
        broadcast(msg,name)
    except:
        user.users_lst["name"].clear()
        socket_obj.close()
        broadcast(f"{name} has left the chat",name)
        return False
        

def server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    addr = (IP,PORT)
    server.bind(addr)

    server.listen()
    print("sever is start....")

    while True:
        # print("accept is calling")
        socket_obj ,ret_addr = server.accept()
        socket_obj.send("Name".encode(FORMAT))
        Name =socket_obj.recv(HEADER).decode(FORMAT)
        
        if not user.check_user(Name):
            socket_obj.send("unknown person".encode(FORMAT))
            socket_obj.close()
            continue

        socket_obj.send(f"salam {Name}".encode(FORMAT))
        broadcast(f'{Name} joined chat:'.encode(FORMAT),Name)
        user.add_conn_obj(Name,socket_obj)
        

        thread = threading.Thread(target=handle_client,args=(socket_obj,ret_addr,Name))
        thread.start()

server()