import structure as structure
from socket import *
from _thread import *
import threading
import datetime

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
serverHost = ''
serverPort = 6789
serverSocket.bind((serverHost,serverPort)) 
serverSocket.listen(1) 
list_of_connections = {}

#def add_user_server(): 
  # recieves string (user name)
  # convert string to user object
  # locate the chat_id in the chats hashtable
  # if user_id exists in chat: 
    # raise an error OR send a diff message to the client
  # else: 
    # insert user id into current chat's user list
    # initialize chat's last_pushed_time to current time
    # send confirmation message back to the client 
    # send_message("wendy added to the chatroom")

#def delete_user_server():
  # recieves string (user name)
  # convert string to user object 
  # locate chat in chats database
  # Remove the chat_id from the user’s list of chats (in the user table)
  # Delete the user sublist in the users dict (in the chat hash table)
  # If the number of users = 0: 
  #   for all users in the chatroom: 
  #     remove the chat id from the user's list of chats
  #   remove the chatname assoc. w/ the chat id 
  #   remove the chat from the chatroom dict
  # client send_message("User, you are not in this chat anymore")
  # send confirmation message back to client. 

def load_chatroom_server(user_id, chatroom_name, conn):
  #get corresponding chat_id from chat_name in Chatnames dictionary
    chatid = structure.Chatnames.get(chatroom_name)
    if chatid == None:
        conn.send("Chatroom does not exist.")
    else:
        #check if this user has this chat
        if chatid in structure.Users.get(user_id).chats:
            #search for chat_id in Chats hash table
            this_chat_obj = structure.Chats.get(chatid)
            #get last_pushed_time of this user
            for user in this_chat_obj.chat_users:
                if user.user_id == user_id:
                    user_time = user.last_pushed_time
                    user.status = 1
                    i = this_chat_obj.chat_users.index(user)
            # get messages after user's last_pushed_time
            m = []
            for msg in this_chat_obj.chat_history:
                if msg.time_stamp > user_time:
                    m.append(msg)
            this_chat_obj.chat_users[i].last_pushed_time = datetime.datetime.now()
            conn.send(str(m).encode())
        else:
            conn.send("You are not a member of this chatroom.")

def send_message_server(user_id, chatroom_name, content, conn):
    # Get current chat_id of client
    chatid = structure.Chatnames.get(chatroom_name)
    if chatroom_name == '':
        conn.send("You are not in any chatroom.")
    else:
        if chatid == None:
            conn.send("Chatroom does not exist.")
        else:
            #search for chat_id in Chats hash table
            this_chat_obj = structure.Chats.get(chatid)
            # Add “client_id, time_stamp = now, message” to history field in chat_id
            this_chat_obj.chat_history.append(structure.Message_obj(user_id,datetime.datetime.now(),content))
            # Push all unread messages to all active users in the chat, change their last_pushed_time to now
            for user in this_chat_obj.chat_users:
                if user.status == 1:
                    user_time = user.last_pushed_time
                    # get messages after user's last_pushed_time
                    m = []
                    for msg in this_chat_obj.chat_history:
                        if msg.time_stamp > user_time:
                            m.append(msg)
                    list_of_connections.get(user.user_id).send(str(m).encode)
                    user.last_pushed_time = datetime.datetime.now()

#def get_my_chats:
  #Get user_id of client
  #Print content of “chats” field for this user in Users hashtable


def threaded(c):
    try:
        message = c.recv(1024)
        if message:
            parsed = message.split(',')
            this_user_id = parsed[0]
            list_of_connections[this_user_id] = c # append to list of connections
            if this_user_id in structure.Users:
                fctn = parsed[-1]
                if fctn == "load_chatroom_client":
                    load_chatroom_server(this_user_id, parsed[1],c)
                elif fctn == "send_message_client":
                    # message body = parsed[1], this chat room = parsed[-2]
                    send_message_server(this_user_id, parsed[-2],parsed[1],c)
    
        #Send response message line into socket
        #c.send(output.encode()) 
        #Send the content of the requested file to the client
        #for i in range(0, len(outputdata)):
            #c.send(outputdata[i].encode())
        c.close()
        else:
            # message may have no content if connection is broken
            # make status of this user 0 in all its chats
    except IOError:
        c.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        c.send(str.encode("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        c.close()



while True:
    #Establish the connection
    print('Ready to serve...')
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    #list_of_connections.append(connectionSocket)
    start_new_thread(threaded,(connectionSocket,))
serverSocket.close()
