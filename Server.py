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

# def user_login_server(username,password,conn): 
#     userObjList = structure.Users.values()
#     for userObj in userObjList: 
#         if (userObj.user_id == username) and (userObj.password == password):
#             conn.send("match")
#         else:
#             conn.send("nomatch")
def add_user_server(user_id, new_user_id, chatroom_name, conn): 
    # 2 people private chat 
    # 3rd person – create a new chatroom 
  chatid = structure.Chatnames.get(chatroom_name)
  this_user_obj = structure.Users.get(new_user_id)
  if chatid == None:
    conn.send("Chatroom does not exist.".encode())  
  this_chat_obj = structure.Chats.get(chatid)
  
  if new_user_id in this_chat_obj.chat_users:  
    conn.send("User is already in chat".encode())
  else: 
    this_chat_obj.chat_users.append(new_user_id) #I'm not sure if this updates the chat's list globally.
    message = ("Added new user {uid} to the chat").format(uid = new_user_id)
    # updates the newly added user's last pushed time 
    this_chat_obj.chat_users[-1].last_pushed_time = datetime.datetime.now() 
    # structure.Chat_user3.last_pushed_time = datetime.datetime.now()  
    
    #add the new chat id to the new user's list of chats
    # structure.Chat_user3.chats.append(chatid)
    
    # update the user's chat list with the chat id
    this_user_obj.chats.append(chatid)

     #send confirmation message back to the client 
    conn.send(message.encode()) 

    #push confirmation message to all users in the chatroom
    send_message_server(new_user_id, chatroom_name, message,conn)
    #when a new user is added to a chat, update chat's name? 

# def delete_user_server(user_id, user_begone_id, chatroom_name,conn):
#   if user_begone_id in structure.demo_chat.chat_users: #replace with current_chat later
#     chatid = structure.Chatnames.get(chatroom_name)
#     # Delete the user sublist in the users dict (in the chat hash table)
#     structure.demo_chat.chat_users.remove(structure.Chat_user_obj('Leah')) #probably a better way to do this
#        # Remove the chat id from the user’s list of chats (in the user table)
#     structure.Chat_user3.chats.remove(chatid)
#     #check # of users
#     if len(structure.demo_chat.chat_users) == 0: 
#       # since there are no users in the chat, we don't need to remove chatid from users list of chats
#       structure.Chatnames.remove(chatroom_name)
#       # remove the chat from the chatroom dict
#       structure.Chats.pop(structure.demo_chat.chat_id) 
#       # client send_message("User, you are not in this chat anymore")
#       message = ("User {uname} is no longer in this chat").format(uname = user_begone_id)
#       conn.send(message.encode())
#       # send confirmation message back to client. 
#     #   send_message_server(user_id, chatroom_name,message,conn)
#   else: 
#     conn.send("User is not in chat.".encode())

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


def get_my_chats_server(user_id,conn):
  #Get user_id of client
    userObj = structure.Users.get(user_id,[])
    if not userObj:
        conn.send("User doesn't exist in the database")
    chats = userObj.chats
    #Print content of “chats” field for this user in Users hashtable
    conn.send(str(chats).encode()) # TO DO: to beautify


def create_chatroom_server(user_id, chat_room_name, other_users,conn):
    # Check if all userIDs are valid
    for user in other_users:
        if user not in structure.Users:
            conn.send("User {} doesn't exist in our database, please check again.".format(user))
            return
    # Create list [thisuserID], append to list al other user IDs entered
    # Append to Chatnames dictionary “chatroom name: new chat id”
    if chat_room_name in structure.Chatnames:
        conn.send("Chat room name {} already exists, please try a new name.".format(chat_room_name))
    chat_id = len(structure.Chatnames) + 1
    structure.Chatnames[chat_room_name] = chat_id
    welcome_message = structure.Message_obj('System',content='Welcome to your new chatroom {}!'.format(chat_room_name))
    
    # create update chatuser_obj for each existing user for the last_pushed_time
    chatuser_obj_list = []
    for user_id in [user_id] + other_users:
        new_chatuser_obj = structure.Chat_user_obj(user_id = user_id, status = 0, last_pushed_time = datetime.datetime.now())
        chatuser_obj_list.append(new_chatuser_obj)
    # Append to Chats “new_chat_id:{users:[[user_id1, status, last_pushed_time], ... , [user_idn,status, last_pushed_time]], history:[]}”, where all last_pushed_time = now
    structure.Chats[chat_id] = structure.Chatroom_obj(chat_id,chatuser_obj_list,[welcome_message])
    # Add new_chat_id to chats list in Users hash table for all involved users
    for user in structure.Users:
        user.chats.append(chat_id)
    # Add to “history” a message “new chat chat_name created” (i.e. [system, time_stamp, message]), send_message([system, time_stamp, message]))
    conn.send("Chatroom creation successful!")
    # broadcast to every usr?

def remove_conn(conn_user_id):
    # make status of this user 0 in all its chats
    if conn_user_id in list_of_connections:
        list_of_connections.Remove(conn_user_id)
        this_user_chats = structure.Users.get(conn_user_id).chats
        for c_id in this_user_chats:
            for user in structure.Chats.get(c_id).chat_users:
                if user.user_id == conn_user_id:
                    user.status = 0

def threaded(c):
    this_user_id = ''
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
                elif fctn == "get_my_chats_client":
                    get_my_chats_server(this_user_id,c)
                elif fctn == "add_user_client": 
                    #user_id = parsed[0], new username = parsed[1], chatroom id = parsed[2], 
                    add_user_server(parsed[0],parsed[1],parsed[2],c)
                # elif fctn == "delete_user_client": 
                #     #user_id = parsed[0], user id to delete = parsed[1], chatroom id = parsed[2]
                #     delete_user_server(parsed[0],parsed[1],parsed[-2])
                # elif fctn == "user_login_client":
                #     user_login_server(parsed[0],parsed[1],c)
    
        #Send response message line into socket
        #c.send(output.encode()) 
        #Send the content of the requested file to the client
        #for i in range(0, len(outputdata)):
            #c.send(outputdata[i].encode())
        else:
            # message may have no content if connection is broken
            # make status of this user 0 in all its chats
            remove_conn(this_user_id)
        c.close()
    except IOError:
        #c.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        #c.send(str.encode("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n","UTF-8"))
        c.close()
        remove_conn(this_user_id)


while True:
    #Establish the connection
    print('Ready to serve...')
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()
    #list_of_connections.append(connectionSocket)
    start_new_thread(threaded,(connectionSocket,))
serverSocket.close()
