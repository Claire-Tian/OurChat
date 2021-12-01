#Users = {user_id1:{chats:[chat_id1, chat_id2, …, chat_idn], status: 0/1 (active/inactive), password: pw_string}}
#Chats = {chat_id1:{users:[[user_id1, status, last_pushed_time], ... , [user_idn,status, last_pushed_time]], history:[[user_id, time_stamp, content_string], [user_id, time_stamp, content_string]]}, chat_id2:{...}}
#Chatnames = [chat_name: chat_id, chat_name2: chat_id2]
import datatime

# define user object used in Users hashtable
class User_obj:
    def __init__(self, user_id = '', password = '', chats = []):
        self.user_id = user_id
        self.password = password
        self.chats = chats

# define object for users in "users" field of Chats hashtable
class Chat_user_obj:
    def __init__(self, user_id = '', status = 0, last_pushed_time = datetime.datetime.now()):
        self.user_id = user_id
        self.status = status
        self.last_pushed_time = last_pushed_time

# define object for chats in Chats hashtable
class Chatroom_obj:
    def __init__(self, chat_id = '', chat_users = [], chat_history = []):
        self.chat_id = chat_id
        self.chat_users = chat_users # a list of chat_user_obj
        self.chat_history = chat_history # a list of chat_obj

# define object for each message in "history" field of Chats hashtable
class Message_obj:
    def __init__(self, user_id = '', time_stamp = datetime.datetime.now(), content = ''):
        self.user_id = user_id
        self.time_stamp = time_stamp
        self.content = content

# define system object
system = User_obj(user_id = 'System', password = 'admin', chats=[])
# define databases
Users = {system.user_id: system}
Chats = {} # format: {Chatroom_obj.chat_id: Chatroom_obj}
Chatnames = {} # format: {chatname: chat_id}
