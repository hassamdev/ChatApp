import socket 
import threading
import pickle
from time import sleep

FORMAT ="utf-8"
# IP = socket.gethostbyname(socket.gethostname())
IP = "localhost"
PORT =4455
HEADER = 1024


class friend_screen:
    def __init__(self,name) -> None:
        self.user_name =name
        self.msg_list =list()

    def add_msg(self,msg):
        self.msg_list.append(msg)





class user:
    def __init__(self,name:str) -> None:
        self.user_name =name
        self.friend_list =list()# friend list sent to the client


    def add_friends(self,user_list:list):
        for user in user_list:
            if user.user_name==self.user_name:
                continue
            self.friend_list.append(friend_screen(user.user_name))

    def __repr__(self) -> str:
        temp =list()
        for frnd in self.friend_list:
            temp.append(frnd.user_name)
        print(self.user_name)
        print(f"friend list {temp}")
        return ""




class users_list:
    def __init__(self) -> None:
        self.users_list =list()


    def add_user(self,user:user):
        self.users_list.append(user)

    def remove_user(self,name:str):
        for user in self.users_list:
            if user.user_name=="name":
                index = self.users_list.index(user)
                self.users_list.remove(index)
                return
        
    def check_user(self,name):
        for u in self.users_list:
            if u.user_name==name:
                return True
            
        return False
    
    def get_friend_lst(self,name):
        for u in self.users_list:
            if u.user_name==name:
                return u.friend_list



hassam = user("hassam")
haider = user("haider")
shams = user("shams")
haroon = user('haroon')

lst =users_list()
lst.add_user(hassam)
lst.add_user(haider)
lst.add_user(shams)
lst.add_user(haroon)


hassam.add_friends(lst.users_list)
haider.add_friends(lst.users_list)
shams.add_friends(lst.users_list)
haroon.add_friends(lst.users_list)

active_users = {}





def handle_msg(_msg,recv):
    sender_name,msg =_msg.split(":")
    for u in lst.users_list:
        if u.user_name ==sender_name:
            for f in u.friend_list:
                if f.user_name==recv:
                    f.msg_list.append(_msg)
                    break

    for u in lst.users_list:
        if u.user_name ==recv:
            for f in u.friend_list:
                if f.user_name==sender_name:
                    f.msg_list.append(_msg)
                    break



def send_to_another_client(_msg,_recv):
    if _recv in active_users:
        active_users[_recv][0].send(_msg.encode(FORMAT))
        return
    return

# def broadcast(msg):
#     for i in user.users_lst:
#         if user.users_lst[i]:
#             user.users_lst[i][0].send(msg.encode(FORMAT))




def handle_client(conn,addr):
    Name =conn.recv(HEADER).decode(FORMAT,errors="ignore")
    print(Name)
    print(type(Name))
        
    if not lst.check_user(Name):
        invalid ="invalid"
        print("invalid")
        conn.send(invalid.encode(FORMAT))
        conn.close()
        return
    valid = "valid"
    print("send valid")
    conn.send(valid.encode(FORMAT))
    print("adding in dic")
    active_users[Name]=[conn]
    sleep(0.5)
        
    frnd_lst = lst.get_friend_lst(Name)
    print(frnd_lst)
    serialized_data = pickle.dumps(frnd_lst)
    conn.send(serialized_data)
    
    # user.add_conn_obj(Name,conn)
    while True:
        try:
            msg =conn.recv(HEADER).decode(FORMAT)
            _msg,recver = msg.split("<*>")
            thread = threading.Thread(target=handle_msg,args=(_msg,recver))
            thread.start()

            send_thread = threading.Thread(target=send_to_another_client,args=(_msg,recver))
            send_thread.start()
        except:
            active_users.pop(Name)
            conn.close()
            
            return False




server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((IP,PORT))

server.listen()
print("server start")


while True:
    conn,addr =server.accept()
    

    thread = threading.Thread(target=handle_client,args=(conn,addr))
    thread.start()