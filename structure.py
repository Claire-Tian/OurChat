#Users = {user_id1:{chats:[chat_id1, chat_id2, …, chat_idn], status: 0/1 (active/inactive), password: pw_string}}
#Chats = {chat_id1:{users:[[user_id1, status, last_pushed_time], ... , [user_idn,status, last_pushed_time]], history:[[user_id, time_stamp, content_string], [user_id, time_stamp, content_string]]}, chat_id2:{...}}
#Chatnames = [chat_name: chat_id, chat_name2: chat_id2]
import datetime

# define user object used in Users hashtable
class User_obj:
    def __init__(self, user_id = '', password = '', chats = []):
        self.user_id = user_id
        self.password = password
        self.chats = chats

# define object for users in "users" field of Chats hashtable
# How do we want to format the last pushed time? 
class Chat_user_obj:
    def __init__(self, user_id = '', status = 0, last_pushed_time = datetime.datetime.now()):
        self.user_id = user_id
        self.status = status
        self.last_pushed_time = last_pushed_time

# define object for chats in Chats hashtable
class Chatroom_obj:
    def __init__(self, chat_id, chat_users = [], chat_history = []):
        self.chat_id = chat_id
        self.chat_users = chat_users # a list of chat_user_obj
        self.chat_history = chat_history # a list of Message_obj

# define object for each message in "history" field of Chats hashtable
class Message_obj:
    def __init__(self, user_id = '', time_stamp = datetime.datetime.now(), content = ''):
        self.user_id = user_id
        self.time_stamp = time_stamp
        self.content = content

# define system object
system = User_obj(user_id = 'System', password = 'admin', chats=[])
# hardcode user objects
# I thought we were using usernames for unique identifiers?
user1 = User_obj('Claire','123',chats=[])
user2 = User_obj('Funing','456',chats=[])
user3 = User_obj('Leah','789',chats=[])
# define system chat
Chat_user1 = Chat_user_obj('Claire')
Chat_user2 = Chat_user_obj('Funing')
Chat_user3 = Chat_user_obj('Leah')
system_hello = Message_obj('System',content='Welcome to Our Chat!')
system_broadcast = Chatroom_obj(0,[Chat_user1,Chat_user2,Chat_user3],[system_hello])
system.chats = system.chats.append(system_broadcast.chat_id)
# define demo user chat (1&2)
demo_user1 = Chat_user_obj('Claire')
demo_user2 = Chat_user_obj('Funing')
demo_chat = Chatroom_obj(1,[demo_user1,demo_user2])
user1.chats = user1.chats.append(demo_chat.chat_id)
user2.chats = user2.chats.append(demo_chat.chat_id)
# define databases
Users = {system.user_id: system, user1.user_id: user1, user2.user_id: user1, user3.user_id: user1}
Chats = {system_broadcast.chat_id:system_broadcast, demo_chat.chat_id:demo_chat} # format: {Chatroom_obj.chat_id: Chatroom_obj}
Chatnames = {'System':0, 'Claire,Funing':1} # format: {chatname: chat_id}
