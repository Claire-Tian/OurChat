import structure as structure
from socket import *
from _thread import *
import threading

serverName = '127.0.0.1'
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

my_user = structure.User_obj('Funing','456',chats=[]) # need to modify after demo, maybe change to a string
my_chat_room = ''

def add_user_client():
   new_user = input("Enter username of the user you want to add to the chat!") #add Leah (lteffera)
   clientSocket.send(my_user.user_id + new_user + my_chat_room + 'add_user_client')
   message = clientSocket.recv(1024) 
   print(('From Server:'), message)

def delete_user_client(): 
  user_begone_id = input("Enter user to delete!")
  clientSocket.send(my_user.user_id + user_begone_id + my_chat_room + 'delete_user_client')
  message = clientSocket.recv(1024) 
  print ('From Server:'), message

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

clientSocket.close()