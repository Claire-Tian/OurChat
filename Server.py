import structure as structure
from socket import *
from _thread import *
import threading
import datetime
import multiprocessing

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a server socket
serverHost = ''
serverPort = 6796
serverSocket.bind((serverHost,serverPort)) 
serverSocket.listen(1) 
list_of_connections = {}
lock = threading.Lock()

# Changed implementation, using lookup with key 
# not using lock methods here, because we aren't writing to structure.py
def login_server(username,password,conn): 
    print("current username and password:",username,type(username),password,type(password))
    retrieved_user = structure.Users.get(username) 
    if retrieved_user!= None and retrieved_user.password == password:
        ack = "1"
        conn.send(ack.encode())
        print("Match, sending 1 back...")
        print("retrieved user user_id + password",retrieved_user.user_id,retrieved_user.password)
    else:
        nak = "0"
        conn.send(nak.encode())
        print("No match, sending 0 back...")
def add_user_server(user_id, new_user_id, chatroom_name,conn,lock): 
    # 2 people private chat 
    # 3rd person,create a new chatroom 
  chatid = structure.Chatnames.get(chatroom_name)
  #create user object for new user
  print(new_user_id)
  this_user_obj = structure.Users.get(new_user_id)
  print("here are the params: ",str([user_id,new_user_id,chatroom_name,conn]))
  print("New user object: ",this_user_obj.user_id,this_user_obj.chats)
  if chatid == None:
    conn.send("Chatroom does not exist.".encode())  
  this_chat_obj = structure.Chats.get(chatid)
  
# would like to be able to view users in chat users list for debugging purposes. 
  chat_users = []
  for obj in this_chat_obj.chat_users:
      chat_users.append(obj.user_id)

  print("Chat object: history, userlist, chat id - ", chat_users,this_chat_obj.chat_id)
  if new_user_id in chat_users:  
    conn.send("User is already in chat".encode())
  else: 
    lock.acquire()
    new_user_obj = structure.Chat_user_obj(new_user_id,datetime.datetime.now())
    this_chat_obj.chat_users.append(new_user_obj)
    print("Chat object update: history, userlist, chat id ", chat_users,this_chat_obj.chat_id)  
    message = ("Added new user {uid} to the chat").format(uid = new_user_id)
    print("message",message)
    lock.release()

    this_user_obj.chats.append(chatid)
    print("New user object update: ",this_user_obj.user_id,this_user_obj.chats)
     #send confirmation message back to the client 
    conn.send(message.encode()) 

    #push confirmation message to all users in the chatroom
    send_message_server(new_user_id, chatroom_name, message,conn)
    #when a new user is added to a chat, update chat's name? 

# todo: account for a) case where # users in chat is 0
# and b) case where user to delete is not in the chat. 
def delete_user_server(user_id, user_begone_id, chatroom_name,conn,lock):
  chatid = structure.Chatnames.get(chatroom_name)
  this_chat_obj = structure.Chats.get(chatid)
  begone_user_obj = structure.Users.get(user_begone_id)
  chat_users_list = []
  for obj in this_chat_obj.chat_users:
      chat_users_list.append(obj.user_id)

  if user_begone_id in chat_users_list: #I need to handle if the user to delete isn't in the list
    lock.acquire()
    # print("deleting user!")
    chat_obj_list = this_chat_obj.chat_users
    count=0
    for obj in chat_obj_list: 
        if obj.user_id == user_begone_id:
            # print("counter rn:",count)
            this_chat_obj.chat_users.remove(this_chat_obj.chat_users[count])
            # print("# users in chat rn, loop",len(this_chat_obj.chat_users))
        count=count+1
    # print("# users in chat rn, loop exited",len(this_chat_obj.chat_users))
    lock.release()
    # print("user deleted!")
    # chat_users_list_2 = []
    # for obj in this_chat_obj.chat_users:
    #   chat_users_list_2.append(obj.user_id)
    
    # print('Current list of users in Claire Funing chat:',str(chat_users_list_2))
    message = ("User {uname} is no longer in this chat").format(uname = user_begone_id)
    conn.send(message.encode())
    send_message_server(user_id, chatroom_name,message,conn)
    
    #check number of users
    # if len(this_chat_obj.chat_users) == 0: 
    #   #remove chatroom name from chatnames
    #   structure.Chatnames.remove(chatroom_name)
    #   # remove the chat from the chatroom dict
    #   structure.Chats.pop(this_chat_obj) 
    #   # client send_message("User, you are not in this chat anymore")
    #   message = ("User {uname} is no longer in this chat").format(uname = user_begone_id)
    #   conn.send(message.encode())
    #   # send confirmation message back to client. 
    #   send_message_server(user_id,chatroom_name,message,conn)
  else:
    conn.send("Sorry, you're not in the group chat.")
def load_chatroom_server(user_id, chatroom_name, conn):
  #get corresponding chat_id from chat_name in Chatnames dictionary
    chatid = structure.Chatnames.get(chatroom_name)
    print("Loading chatroom: ",chatroom_name)
    if chatid == None:
        conn.send(b"Chatroom does not exist.")
    else:
        #check if this user has this chat
        if chatid in structure.Users.get(user_id).chats:
            #search for chat_id in Chats hash table
            this_chat_obj = structure.Chats.get(chatid)
            #get last_pushed_time of this user
            for user in this_chat_obj.chat_users:
                if user.user_id == user_id:
                    print("User ID before load: ",user.user_id)
                    print("User Status before load: ",user.status)
                    user_time = user.last_pushed_time
                    lock.acquire()
                    user.status = 1
                    lock.release()
                    print("User status after load: ",user.status)
                    i = this_chat_obj.chat_users.index(user)
                    # get messages after user's last_pushed_time
                    m = []
                    for msg in this_chat_obj.chat_history:
                        if msg.time_stamp > user_time:
                            m.append(str(msg) + "\n")
                    lock.acquire()
                    this_chat_obj.chat_users[i].last_pushed_time = datetime.datetime.now()
                    lock.release()
                    conn.send(str(m).encode())
            print("loaded chatroom")
        else:
            conn.send(b"You are not a member of this chatroom.")

def send_message_server(user_id, chatroom_name, content, conn):
    # Get current chat_id of client
    print("Current user ID: ",user_id)
    chatid = structure.Chatnames.get(chatroom_name)
    print("Current chatroom name: ",chatroom_name)
    #print(structure.Chatnames)
    #print(chatid)
    if chatroom_name == '':
        conn.send(b"You are not in any chatroom.")
    else:
        if chatid == None:
            conn.send(b"Chatroom does not exist.")
        else:
            #search for chat_id in Chats hash table
            this_chat_obj = structure.Chats.get(chatid)
            lock.acquire()
            this_chat_obj.chat_history.append(structure.Message_obj(user_id,datetime.datetime.now(),content))
            lock.release()
            # Push all unread messages to all active users in the chat, change their last_pushed_time to now
            #print(this_chat_obj.chat_history)
            for user in this_chat_obj.chat_users:
                print("User ID: ",user.user_id)
                print("User status in send: ",user.status)
                if user.status == 1:
                    user_time = user.last_pushed_time
                    #print("in for loop")
                    # get messages after user's last_pushed_time
                    m = []
                    for msg in this_chat_obj.chat_history:
                        #print(str(msg))
                        if msg.time_stamp > user_time:
                            m.append(str(msg) + "\n")
                    print("Message to push:",m)
                    conn_i = list_of_connections.get(user.user_id)
                    to_send = str(m)
                    conn_i.send(to_send.encode())
                    lock.acquire()
                    user.last_pushed_time = datetime.datetime.now()
                    lock.release()
                    print("sent to " + user.user_id)


def get_my_chats_server(user_id,conn):
  #Get user_id of client
    userObj = structure.Users.get(user_id,[])
    if not userObj:
        conn.send("User doesn't exist in the database".encode())
    chats = userObj.chats
    user_chatnames = []
    for chat in chats:
        for cn in structure.Chatnames:
            if structure.Chatnames[cn] == chat:
                print(cn)
                user_chatnames.append(cn)
    print('user chatnames: ',user_chatnames)
    user_chatnames = list(set(user_chatnames))
    conn.send(str(user_chatnames).encode())


def create_chatroom_server(user_id, chat_room_name, other_users,conn):
    # Check if all userIDs are valid
    for user in other_users:
        if user not in structure.Users:
            conn.send("User {} doesn't exist in our database, please check again.".format(user))
            return
    # Create list [thisuserID], append to list al other user IDs entered

    if chat_room_name in structure.Chatnames:
        conn.send("Chat room name {} already exists, please try a new name.".format(chat_room_name))
    chat_id = len(structure.Chatnames)
    lock.acquire()
    structure.Chatnames[chat_room_name] = chat_id
    welcome_message = structure.Message_obj('System',content='Welcome to your new chatroom {}!'.format(chat_room_name))
    
    # create update chatuser_obj for each existing user for the last_pushed_time
    chatuser_obj_list = []
    for user_id in [user_id] + other_users:
        new_chatuser_obj = structure.Chat_user_obj(user_id = user_id, last_pushed_time = datetime.datetime.now())
        chatuser_obj_list.append(new_chatuser_obj)

    structure.Chats[chat_id] = structure.Chatroom_obj(chat_id,chatuser_obj_list,[welcome_message])
    # Add new_chat_id to chats list in Users hash table for all involved users
    for user in structure.Users:
        print("location of each user's chat: ", hex(id(structure.Users.get(user).chats)))
        structure.Users.get(user).chats.append(chat_id)
    lock.release()

    conn.send(b"Chatroom creation successful!")
    # broadcast to every usr?
    print("Chats database after create: ", structure.Chats)
    print("Chatnames database after create: ", structure.Chatnames)

def remove_conn(conn_user_id):
    # make status of this user 0 in all its chats
    lock.acquire()
    if conn_user_id in list_of_connections:
        list_of_connections.pop(conn_user_id)
        #lock.release()
        this_user_chats = structure.Users.get(conn_user_id).chats
        for c_id in this_user_chats:
            for user in structure.Chats.get(c_id).chat_users:
                if user.user_id == conn_user_id:
                    #lock.acquire()
                    user.status = 0
    lock.release()

def threaded(c):
    lock = multiprocessing.Lock()
    this_user_id = ''
    #print("in threaded")
    while True:
        try:
            message = c.recv(1024).decode()
            #print(message)
            if message:
                parsed = message.split(',')
                this_user_id = parsed[0]
                lock.acquire()
                list_of_connections[this_user_id] = c # append to list of connections
                lock.release()
                if this_user_id in structure.Users:
                    fctn = parsed[-1]
                    if fctn == "load_chatroom_client":
                        load_chatroom_server(this_user_id, parsed[1],c)
                    elif fctn == "send_message_client":
                        # message body = parsed[1], this chat room = parsed[-2]
                        #print("in threaded function")
                        #print(parsed[-2])
                        send_message_server(this_user_id, parsed[-2],parsed[1],c)
                    elif fctn == "get_my_chats_client":
                        get_my_chats_server(this_user_id,c)
                    elif fctn == "add_user_client":
                        print("here's what parsed looks like:" + "parsed: " + parsed[0] + "," + parsed[1] + "," + parsed[2])
                        print(type(parsed[0]),type(parsed[1]),type(parsed[2]))
                        add_user_server(parsed[0],parsed[1],parsed[2],c,lock)
                    elif fctn == "delete_user_client":
                        delete_user_server(parsed[0],parsed[1],parsed[2],c,lock)
                    elif fctn == "login_client":
                        login_server(parsed[0],parsed[1],c)
                    elif fctn == "create_chatroom_client":
                        o_users = []
                        for i in range(2,len(parsed)-1):
                            o_users.append(parsed[i])
                        create_chatroom_server(this_user_id, parsed[1], o_users,c)
                    elif fctn == "quit":
                        c.close()

    
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
