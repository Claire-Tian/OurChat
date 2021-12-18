import structure as structure
from socket import *
from _thread import *
import threading
import sys
import queue

serverName = '149.130.169.118'
serverPort = 6789
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
# additional protocol & new socket dedicated to listen, server be able to know which is which


my_user = structure.User_obj('Claire','123') # need to modify after demo, maybe change to a string
my_chat_room = ''

'''def listen_for_messages():
    while True:
        message = clientSocket.recv(1024).decode()
        print("\n" + message)'''

# make a thread that listens for messages to this client & print them
#t = threading.Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
#.daemon = True
# start the thread
#t.start()


#def receive_msg():
    #while True:
        #try:
            #msg = clientSocket.recv(1024).decode()
            #print(msg)
        #except Exception as err:
            #return err

def add_user_client():
   new_user = input("Enter username of the user you want to add to the chat!") #add Leah (lteffera)
   clientSocket.send(my_user.user_id + new_user + my_chat_room + 'add_user_client')
   message = clientSocket.recv(1024) 
   print(('From Server:'), message)

def delete_user_client(): 
  user_begone_id = input("Enter user to delete!")
  clientSocket.send()
  message = clientSocket.recv(1024) 
  print ('From Server:'), message

def load_chatroom_client(): 
   #print("in load chatroom client")
   chatroom_name = input("Please enter a chatroom name: ")
   input_str = my_user.user_id + "," + chatroom_name + "," + "load_chatroom_client"
   clientSocket.send(input_str.encode())
   global my_chat_room
   #print('chat room name in load_chat_room_client before recv: ',my_chat_room)
#   # server side code, returns chatroom
   message = clientSocket.recv(1024)
   my_chat_room = chatroom_name
   print("***************************************************")
   print('Current chatroom: ',my_chat_room)
   print("Unread messages: ")
   print(message)

def send_message_client(my_user):
    #s = str("(" + my_user.user_id + ") > ")
    chat_message = input("(Claire) > ")
    #print('chat room name in send message client: ',my_chat_room)
    input_str = my_user.user_id + "," + chat_message + ','+ my_chat_room + "," + "send_message_client"
    #print('send_message_client input str ',input_str)
    clientSocket.send(input_str.encode())
    #print('sending chat_message to the server: ',chat_message)
    message = clientSocket.recv(1024)
    print(message.decode())
    chat_message = input("(Claire) > ")
    print('')
    #return True

    
def create_chatroom_client(my_user):
    usernames = []
    chatroom_name = input("Please enter a name for your chatroom: ")
    username = input("Please enter a username that you'd like to add in your chatroom, Write the single character q to quit.")
    while username != "q":
        usernames.append(username)
   # for every username recieved from client input:
   #   add user to list of usernames
   # clientSocket.send(chatroom_name)
    input_str = my_user.user_id + "," + chatroom_name + "," + ",".join(usernames) + "," + "create_chatroom_client"
    clientSocket.send(input_str.encode())
    message = clientSocket.recv(1024) 
    print ('From Server:', message)
    if message == "Chatroom creation successful!":
       # move client's status to the new chatroom
        my_chat_room = chatroom_name

def get_my_chats_client(my_user):
  #sent back a list of chatrooms from server, which are displayed in terminal
  input_str = my_user.user_id + "," + "get_my_chats_client"
  clientSocket.send(input_str.encode())
  message = clientSocket.recv(1024)
  print(message.decode())

def login_client():
    pass

command_dict = {"login":login_client,"add_user":add_user_client,"delete_user":delete_user_client,
    "load":load_chatroom_client, "send":send_message_client,"create_chatroom":create_chatroom_client,
    "get_my_chats":get_my_chats_client}
print("Welcome to OurChat, an interactive messaging system on your command line!")
print("Available commands are: \n To load a chatroom: type load; \n To send a message: type send; \n To create a chatroom: type create_chatroom \n"+
"To add a user: type add_user; \n to delete a user: type delete_user; \n to get a list of your chatrooms: type get_my_chat\n")
print("To continue, please enter one of the following commands below, type q to quit. \n")
#cmd_queue = queue.Queue()
#stdout_lock = threading.Lock()
#dj = threading.Thread(target=console, args=(cmd_queue, ))
#dj.start()

while True:
    
    #print("To load a chatroom: type load_chatroom_client; To send a message: type send_message_client; To create a chatroom: type create_chatroom_client \n")
    #print("To add a user: type add_user_client; to delete a user: type delete_user_client")
    
    #user_input = input("To continue, please enter one of the following commands below, type q to quit. \n")
    
    #cmd = cmd_queue.get()
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
        "To create a chatroom: type create_chatroom; \n"+
        "To add a user: type add_user; \n to delete a user: type delete_user; \n to get a list of your chatrooms: type get_my_chat \n")
    elif cmd == "add_user":
        action()
    elif cmd == "delete_user":
        action()
    elif cmd == "load":
        #print("in while loop")
        action()
    elif cmd == "send":
        #receive_thread = threading.Thread(target=receive_msg)
        #receive_thread.start()
        action(my_user)
        #new_thread = threading.Thread(target=action(my_user))
        #new_thread.start()
        #boolean = action(my_user)
        #while True:
            #boolean = action(my_user)
            #if boolean == False:
            #    break
    elif cmd == "create_chatroom":
        action(my_user)
    elif cmd == "get_my_chats":
        action(my_user)

    
    #action(stdout_lock)


clientSocket.close()