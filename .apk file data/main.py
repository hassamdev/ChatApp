from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivy.core.window import Window
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton,MDFlatButton
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList,OneLineAvatarIconListItem
from kivymd.theming import ThemeManager
from kivymd.uix.list.list import ImageLeftWidget
from kivymd.uix.textfield import MDTextField
import threading,socket
from kivymd.toast import toast
from kivy.clock import Clock
import pickle
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel






FORMAT ="utf-8"
IP = '3.6.115.182'
PORT =18217
HEADER =1024


class friend_screen:



    def __init__(self,name) -> None:
        self.user_name =name
        self.msg_list =list()




    def add_msg(self,msg):
        self.msg_list.append(msg)



class data():




    def __init__(self,**kwargs):
        self.id = None
        self.name = None
        self.email =None
        self.design =None
        self.ip = None
        self.DOB = None




    def set_data(self,_id=None,_name=None,_email=None,ip=None,_DOB=None,_design=None):
        self.id = _id
        self.name = _name
        self.email = _email        
        self.ip = ip
        self.DOB = _DOB
        self.design =_design




    def set_empty(self):
        self.id = ""
        self.name =""
        self.email = ""        
        self.ip = ""
        self.DOB = ""
        self.design =""






############################################101 inbox screen





class inbox_screen(Screen):




    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.head = None
        
        self.scrol_view = MDScrollView(pos_hint = {"center_x": 0.5,"center_y":0.5})
        self.scrol_view.size_hint_y=0.8
        self.add_widget(self.scrol_view)

        self.message_container = None
        self.actual_message_list =list()
        self.data = data()
        self.last_view =None
        self.check =False
        self.notify = False
        

        self.message_field= None
        self.foot=None
        self.msg_lst_size = 0
        self.message_list = list()


        self.header()
        self.footer()
        Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}
        Window.softinput_mode = "below_target"
        

    

    def header(self):
        app = MDApp.get_running_app()
        self.head = MDTopAppBar(
        title= self.name,
        # right_action_items= [["dots-vertical"]],
        left_action_items = [['arrow-left',self.back]],
        pos_hint = {"center_x": 0.5,"center_y":0.95}
        )
        self.head.md_bg_color=(0.2,0.2,0.2,1)
        
        self.add_widget(self.head)




    def footer(self):
        self.foot = MDBoxLayout(
        # right_action_items= [["send",self.send_msg]],
        pos_hint = {"center_x": 0.5,"center_y":0.06},
        size_hint=(1,0.1)
        )
        # self.foot.md_bg_color=(0.2,0.2,0.2,1)
        self.message_field = MDTextField(hint_text='Type a message',
                                    multiline=True,
                                    size_hint=(1, 0.1),
                                    max_height= "70dp",
                                    pos_hint = {"center_x": 0.5,"center_y":0.5},
                                    mode = "fill"
                                    )
        self.message_field.fill_color_normal=(0.2,0.2,0.2,1)
        self.message_field.bind(focus=self.on_focus)
        self.foot.add_widget(self.message_field) 
        self.add_widget(self.foot)

        send_button = MDIconButton(
            icon= "send",
            line_color= (0, 0, 0, 0),
            pos_hint= {"center_x": .5, "center_y": .5},
            size_hint = (0.15,None),
            on_release =self.send_msg
            )
        self.foot.add_widget(send_button)





    def on_focus(self,instance,value):
        if value:
            # When the TextInput gains focus, move the layout up
            self.size_hint_y = 0.6
            self.pos_hint={"center_x":0.5,"center_y":0.35}
        else:
            # When the TextInput loses focus, reset the layout position
            self.size_hint_y = 1
            self.pos_hint={"center_x":0.5,"center_y":0.5}
        




    def back(self,event):
        app = MDApp.get_running_app()        
        app.scrn_manager.current = 'chatting'
        
        if self.notify:
            app.chat.remove_notification(self.name)
    
        self.check = False
        self.notify = False
        

    



    def create_msg_lst(self):
        app = MDApp.get_running_app()

        self.message_container = MDBoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        self.message_container.bind(minimum_height=self.message_container.setter('height'))

        self.scrol_view.add_widget(self.message_container)
        
        for msg in self.actual_message_list:
            _name,_msg =msg.split(":")
            if _name == app.name_of_owner:
                label = MDLabel(text = msg,size_hint=(None,None),theme_text_color="ContrastParentBackground"
                                                      ,size = (300,50))
                with label.canvas.before:
                    Color(1,1,1,0.75)
                label.md_bg_color =(1,1,1,0.75)
                self.message_container.add_widget(label)
            else:
                label = MDLabel(text = msg,size_hint=(None,None),theme_text_color="ContrastParentBackground"
                                                      ,size = (300,50))
                with label.canvas.before:
                    Color(0,1,0,0.5)
                label.md_bg_color =(0,1,0,0.5)
                self.message_container.add_widget(label)

            self.msg_lst_size += 1
        
        Clock.schedule_interval(self.automate, 0.5)

        




    def send_msg(self,event):
        app=MDApp.get_running_app()
        message = self.message_field.text
        # connect_to_peer(self.data.ip,5050,message)
        try:
            app.client.send(f"{app.name_of_owner}: {message}<*>{self.name}".encode(FORMAT))
        except:
            toast("server is offline")
        self.message_field.text =""
        self.actual_message_list.append(f"{app.name_of_owner}: {message}")
        





    def automate(self,event):
        app =MDApp.get_running_app()
    
        if len(self.actual_message_list)>self.msg_lst_size:
            msg = self.actual_message_list[-1]
            _name,_msg = msg.split(":")
            self.msg_lst_size += 1
            if _name == app.name_of_owner:
                label = MDLabel(text = msg,size_hint=(None,None),theme_text_color="ContrastParentBackground"
                                                        ,size = (300,50))
                with label.canvas.before:
                    Color(1,1,1,0.75)
                label.md_bg_color =(1,1,1,0.75)
                self.message_container.add_widget(label)

            else:
                label = MDLabel(text = msg,size_hint=(None,None),theme_text_color="ContrastParentBackground"
                                                        ,size = (300,50))
                with label.canvas.before:
                    Color(0,1,0,0.5)
                label.md_bg_color =(0,1,0,0.5)
                self.message_container.add_widget(label)
        
            if not self.check:
                if not self.notify:
                    app.chat.show_notification(self.name)
                    self.notify=True
                
            

        
    

    






##########################################101 chatting screen




class chatting(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.box = None
        self.scrol_view = None
        self.client = None
        self.right_noti_widget=None

        self.header()
        self.scroll_view()






    def header(self):
        self.box = MDTopAppBar(
        title= 'Chat App',
        # right_action_items= [["camera"],["magnify"], ["dots-vertical"]],
        # specific_text_color= app.theme_cls.accent_color,
        pos_hint = {"center_x": 0.5,"center_y":0.95}
        )
        self.box.md_bg_color=(0.2,0.2,0.2,1)
        # self.box.pos_hint(0.5,0.8)

        
        self.add_widget(self.box)






    def scroll_view(self):
        app = MDApp.get_running_app()
        self.scrol_view = MDScrollView(pos_hint = {"center_x": 0.5,"center_y":0.4})
        self.md_list = MDList()

        for user in app.friend_list:
             
            self.md_list.add_widget(
                OneLineAvatarIconListItem(ImageLeftWidget(source="avatar.png"),

                                    text=f"Name:{user.user_name}",
                                    on_release =self.call,
                                ))
            

        self.scrol_view.add_widget(self.md_list)
        self.add_widget(self.scrol_view)
        # self.show_notification()





    def show_notification(self,name):
        for item in self.md_list.children:
            if item.text ==f"Name:{name}":
                item.theme_text_color = "Custom"
                item.text_color = (0, 1, 0, 1)
                return





    def remove_notification(self,name):
        for item in self.md_list.children:
            if item.text ==f"Name:{name}":
                item.theme_text_color = "Custom"
                item.text_color = (1, 1, 1, 1)              
                return
                





    def call(self,event):
        app = MDApp.get_running_app()
        # print("text is ",event.secondary_text)

        extra ,name= event.text.split(":")
        app.scrn_manager.current = name
        currnt_scrn= app.scrn_manager.get_screen(name)
        currnt_scrn.check = True



#######################################################101 enter_name class





class name(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.message_field = MDTextField(hint_text='Type your name..',
                                    size_hint=(0.75, 0.1),
                                    pos_hint = {"center_x": 0.5,"center_y":0.5},
                                    mode = "fill"
                                    )
        self.message_field.fill_color_normal=(0.2,0.2,0.2,1)
        self.add_widget(self.message_field) 
        

        send_button = MDFlatButton(
            text="connect",
            line_color= (0, 0, 0, 0),
            pos_hint= {"center_x": .5, "center_y": .4},
            size_hint = (0.15,None),
            on_release = self.connect
            )
        self.add_widget(send_button)






    def connect(self,event):
        app = MDApp.get_running_app()
        name =self.message_field.text
        if name=="":
            toast("please enter the name...")
            return
        
        try:    
            app.connect_to_server()
        except:
            toast("server is offline")
            return
        app.client.send(name.encode(FORMAT))

        
        msg =app.client.recv(HEADER).decode(FORMAT,errors="ignore")
        if msg=="invalid":
            toast("wrong username,connection failed")
            app.close_connection()
            return
        elif msg=="valid":
            data = app.client.recv(4096)
            print(data)
            friend_list = pickle.loads(data)
            
            app.set_name(name)
            app.add_user_list(friend_list)
            app.create_screens()
            app.create_thread()
            app.scrn_manager.current = "chatting"
            return
        toast("server is offline")
        return
                





#######################################################101 main app class




class ITX_SOLUTION(MDApp):


    def build(self):
        Window.size = (360, 640)

        theme = ThemeManager()
        theme.theme_style = 'Dark'
        self.theme_cls=theme
        self.friend_list =None
        self.name_of_owner =None
        self.client =None
        
        
        self.stop_event = threading.Event()

        self.scrn_manager  = ScreenManager()

        self.enter_name_scr =name(name="name")
        self.scrn_manager.add_widget(self.enter_name_scr)
        
        # start_sever()
        self.inbox = None

        return self.scrn_manager
    




    def add_to_inbox(self,msg):
        print("add_to_inbox is called")
        _name,_msg= msg.split(":")
        for i in self.scrn_manager.screens:
            if i.name ==_name:
                i.actual_message_list.append(msg)
                return
            



    def recv_msg(self):
        while True:
            try:
                msg = self.client.recv(HEADER).decode(FORMAT)
                self.add_to_inbox(msg)
                
            except:
                print("if error")
                try:
                    toast('connection failed')
                    self.client.close()
                except:
                    pass
                return



    def create_thread(self):
        thread = threading.Thread(target=self.recv_msg)
        thread.start()

    


    def set_name(self,name):
        self.name_of_owner = name
    



    def add_user_list(self,frnd_lst):
        self.friend_list = frnd_lst

    



    def create_screens(self):
        self.chat = chatting(name="chatting")
        self.scrn_manager.add_widget(self.chat)
        

        for f in self.friend_list:
            inbox =inbox_screen(name=f.user_name)
            inbox.actual_message_list = f.msg_list
            inbox.create_msg_lst()
            self.scrn_manager.add_widget(inbox)


            


    def connect_to_server(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect((IP,PORT))
        




    def close_connection(self):
        self.client.close()
        del self.client





    def on_stop(self):
        self.stop_event.set()
        if self.client:
            self.close_connection()
        # self.network.SERVER.shutdown(socket.SHUT_RDWR)
        # SERVER.close()
        
            

    
app = ITX_SOLUTION()
app.run()