import socket 
import threading

FORMAT ="utf-8"
IP = socket.gethostbyname(socket.gethostname())
PORT =5050
HEADER = 1024



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

def broadcast(msg):
    for i in user.users_lst:
        if user.users_lst[i]:
            user.users_lst[i][0].send(msg.encode(FORMAT))

def handle_client(conn,addr):
    conn.send("Name".encode(FORMAT))
    Name =conn.recv(HEADER).decode(FORMAT)
        
    if not user.check_user(Name):
        conn.send("unknown person".encode(FORMAT))
        conn.close()
        return
        

    conn.send(f"salam {Name}".encode(FORMAT))
    broadcast(f'{Name} joined chat:')
    user.add_conn_obj(Name,conn)
    while True:
        try:
            msg =conn.recv(HEADER).decode(FORMAT)
            broadcast(msg)
        except:
            user.users_lst[Name].clear()
            conn.close()
            broadcast(f"{Name} has left the chat")
            return False

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((IP,PORT))

server.listen()
print("server start")


while True:
    conn,addr =server.accept()
    

    thread = threading.Thread(target=handle_client,args=(conn,addr))
    thread.start()
    