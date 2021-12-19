import structure as structure
from socket import *
from _thread import *
import threading
import sys
import queue
import multiprocessing

serverName = '192.168.1.168'
serverPort = 6795
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
# additional protocol & new socket dedicated to listen, server be able to know which is which
lock = threading.Lock()

my_user = structure.User_obj('Funing','456') # need to modify after demo, maybe change to a string
my_chat_room = ''

'''def listen_for_messages():
    while True:
        message = clientSocket.recv(1024).decode()
        print("\n" + message)'''

def add_user_client():
   new_user = input("Enter username of the user you want to add to the chat!") 
   input_str = my_user.user_id + "," + new_user + "," + "Claire Funing" + "," + "add_user_client"
   clientSocket.send(input_str.encode())
   message = clientSocket.recv(1024) 
   print(('From Server:'), message.decode())

def delete_user_client(): 
  user_begone_id = input("Enter user to delete!")
  clientSocket.send(my_user.user_id + "," + user_begone_id + "," + "Claire Funing" + "," + "delete_user_client")
  message = clientSocket.recv(1024) 
  print(('From Server:'), message)

def load_chatroom_client(): 
   #print("in load chatroom client")
   chatroom_name = input("Please enter a chatroom name: ")
   input_str = my_user.user_id + "," + chatroom_name + "," + "load_chatroom_client"
   clientSocket.send(input_str.encode())
   #print('chat room name in load_chat_room_client before recv: ',my_chat_room)
#   # server side code, returns chatroom
   message = clientSocket.recv(1024)
   lock.acquire()
   global my_chat_room
   my_chat_room = chatroom_name
   lock.release()
   print("***************************************************")
   print('Current chatroom: ',my_chat_room)
   print("Unread messages: ")
   print(message)

def send_message_client():
    #s = str("(" + my_user.user_id + ") > ")
    chat_message = input("({}) > ".format(my_user.user_id))
    print('')
    #print('chat room name in send message client: ',my_chat_room)
    input_str = my_user.user_id + "," + chat_message + ','+ my_chat_room + "," + "send_message_client"
    #print('send_message_client input str ',input_str)
    clientSocket.send(input_str.encode())
    #print('sending chat_message to the server: ',chat_message)
    message = clientSocket.recv(1024)
    print(message.decode())
    #return True

    
def create_chatroom_client():
    usernames = []
    chatroom_name = input("Please enter a name for your chatroom: ")
    username = input("Please enter a list of usernames that you'd like to add in your chatroom, deliminated by \';\': ")
    usernames = username.split(';')
   # for every username recieved from client input:
   #   add user to list of usernames
   # clientSocket.send(chatroom_name)
    input_str = my_user.user_id + "," + chatroom_name + "," + ",".join(usernames) + "," + "create_chatroom_client"
    clientSocket.send(input_str.encode())
    message = clientSocket.recv(1024) 
    print ('From Server:', message.decode())
    if message.decode() == "Chatroom creation successful!":
       # move client's status to the new chatroom
        lock.acquire()
        global my_chat_room
        my_chat_room = chatroom_name
        lock.release()
    print("***************************************************")
    print('Current chatroom: ',my_chat_room)

def get_my_chats_client():
  #sent back a list of chatrooms from server, which are displayed in terminal
  input_str = my_user.user_id + "," + "get_my_chats_client"
  clientSocket.send(input_str.encode())
  message = clientSocket.recv(1024)
  print(message.decode())

def login_client():
    #enter in your username, password like "Leah,789",please include the comma.
    username,password = input("To log in, please enter your username,password").split(",")
    clientSocket.send(username + "," + password + "," + "login_client")
    message = clientSocket.recv(1024) 
    print("From Server:", message.decode()) 
    if message.decode() == "1": 
        print("You,{name},are now logged in!".format(name=username))
        my_user = structure.Users.get(username)
        print('My user:',my_user,my_user.user_id,my_user.password,str(my_user.chats))
    elif message.decode() == "0": 
        print("Sorry, looks like you aren't in the system.") 


command_dict = {"login":login_client,"add_user":add_user_client,"delete_user":delete_user_client,
    "load":load_chatroom_client, "send":send_message_client,"create":create_chatroom_client,
    "get_my_chats":get_my_chats_client}
print("Welcome to OurChat, an interactive messaging system on your command line!")
print("Available commands are: \n To load a chatroom: type load; \n To send a message: type send; \n To create a chatroom: type create \n"+
"To add a user: type add_user; \n to delete a user: type delete_user; \n to get a list of your chatrooms: type get_my_chat\n To login: type login")
print("To continue, please enter one of the following commands below, type q to quit. \n")

while True:
    cmd = input('> ')
    if cmd == 'q':
        s = my_user.user_id + ", quit"
        clientSocket.send(s.encode())
        clientSocket.close()
        break
    action = command_dict.get(cmd, "invalid_input")
    if cmd == "invalid_input":
        print("Invalid input, please try again")
        print("Available commands are: \n To load a chatroom: type load; \n To send a message: type send; \n" + 
        "To create a chatroom: type create; \n"+
        "To add a user: type add_user; \n to delete a user: type delete_user; \n to get a list of your chatrooms: type get_my_chat \n")
    elif cmd == "add_user":
        action()
    elif cmd == "delete_user":
        action()
    elif cmd == "load":
        action()
    elif cmd == "send":
        action()
    elif cmd == "create":
        action()
    elif cmd == "get_my_chats":
        action()
    elif cmd == "login":
        action()

    
    #action(stdout_lock)

clientSocket.close()