import structure as structure
from socket import *
from _thread import *
import threading
import sys

serverName = '127.0.0.1'
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


my_user = structure.User_obj('Funing','456',chats=[]) # need to modify after demo, maybe change to a string
my_chat_room = ''

# def user_login_client():
#    #maybe use a while loop? while loggedin = false,
#    logged_in = False
#    while logged_in == False:
#       username,password = ("To log in, please enter your username,password").split(",")
#       clientSocket.send(username + "," + password + "," + "user_login_client")
#       message = clientSocket.recv(1024)
#       print(('From Server:'), message) #depending on message, toggle loggedin to be true
#       if message == "match": 
#          logged_in = True
#       elif message == "nomatch": 
#          print("Sorry, looks like you aren't in the system.")
#          break

def add_user_client(my_user):
   new_user = input("Enter username of the user you want to add to the chat!") #add Leah (lteffera)
   clientSocket.send(my_user.user_id + "," + new_user + "," + my_chat_room + "," + 'add_user_client')
   message = clientSocket.recv(1024) 
   print(('From Server:'), message)

def delete_user_client(my_user): 
  user_begone_id = input("Enter user to delete!")
  clientSocket.send(my_user.user_id + "," + user_begone_id + "," + my_chat_room + "," + 'delete_user_client')
  message = clientSocket.recv(1024) 
  print(('From Server:'), message)

def load_chatroom_client(my_user): 
   chatroom_name = input("Please enter a chatroom name: ")
   clientSocket.send(my_user.user_id + "," + chatroom_name + "," + "load_chatroom_client")
#   # server side code, returns chatroom
   message = clientSocket.recv(1024)
   my_chat_room = chatroom_name 
   print(message)

def send_message_client(my_user):
    chat_message = input("Please enter your chat message: ")
    clientSocket.send(my_user.user_id + "," + chat_message + ','+ my_chat_room + "," + "send_message_client")
    message = clientSocket.recv(1024)
    print(message)

    
def create_chatroom_client(my_user):
    usernames = []
    chatroom_name = input("Please enter a name for your chatroom: ")
    username = input("Please enter a username that you'd like to add in your chatroom, Write the single character q to quit.")
    while username != "q":
        usernames.append(username)
   # for every username recieved from client input:
   #   add user to list of usernames
   # clientSocket.send(chatroom_name)
    clientSocket.send(my_user.user_id + "," + chatroom_name + "," + ",".join(usernames) + "," + "create_chatroom_client")
    message = clientSocket.recv(1024) 
    print ('From Server:', message)
    if message == "Chatroom creation successful!":
       # move client's status to the new chatroom
        my_chat_room = chatroom_name

def get_my_chats_client(my_user):
  #sent back a list of chatrooms from server, which are displayed in terminal
  clientSocket.send(my_user.user_id + "," + "get_my_chats_client")
  message = clientSocket.recv(1024)
  print(message)

def login_client():
    pass

cmd_queue = queue.Queue()
stdout_lock = threading.Lock()
dj = threading.Thread(target=console, args=(cmd_queue, stdout_lock))
dj.start()

while True:
    command_dict = {"login":login_client,"add_user_client":add_user_client,"delete_user_client":delete_user_client,
    "load_chatroom_client":load_chatroom_client, "send_message_client":send_message_client,"create_chatroom_client":create_chatroom_client}
    print("Welcome to OurChat, an interactive messaging system on your command line!")
    print("Available commands are: \n To load a chatroom: type load_chatroom_client; To send a message: type send_message_client; To create a chatroom: type create_chatroom_client \n"+
    "To add a user: type add_user_client; to delete a user: type delete_user_client")
    #print("To load a chatroom: type load_chatroom_client; To send a message: type send_message_client; To create a chatroom: type create_chatroom_client \n")
    #print("To add a user: type add_user_client; to delete a user: type delete_user_client")
    
    user_input = input("To continue, please enter one of the following commands below, type q to quit")

    cmd = cmd_queue.get()
    if cmd == 'q':
        break
    action = cmd_actions.get(cmd, "invalid_input")
    if cmd == "invalid_input":
        print("Invalid input, please try again")
        print("Available commands are: \n To load a chatroom: type load_chatroom_client; To send a message: type send_message_client; To create a chatroom: type create_chatroom_client \n"+
    "To add a user: type add_user_client; to delete a user: type delete_user_client")
    elif cmd == "add_user_client":
        action()
    elif cmd == "delete_user_client":
        action()
    elif cmd == "load_chatroom_client":
        action(my_user)
    elif cmd == "send_message_client":
        action(my_user)
    elif cmd == "create_chatroom_client":
        action(my_user)


    
    action(stdout_lock)

clientSocket.close()