
from typing import Any

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


hassam = user("hassam")
haider = user("haider")

lst =users_list()
lst.add_user(hassam)
lst.add_user(haider)

hassam.add_friends(lst.users_list)
haider.add_friends(lst.users_list)

print(hassam)
print(haider)