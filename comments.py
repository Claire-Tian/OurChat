#console

#input()  
        #with lock:

#send message client: 

    #if chat_message == 'q':
    #    return False

    '''while chat_message != 'q':
        print('chat room name in send message client: ',my_chat_room)
        input_str = my_user.user_id + "," + chat_message + ','+ my_chat_room + "," + "send_message_client"
        print('send_message_client input str ',input_str)
        clientSocket.send(input_str.encode())
        print('sending chat_message to the server: ',chat_message)
        message = clientSocket.recv(1024)
        chat_message = input("Please enter your chat message: ")
        print(message.decode())'''

#create chatroom client: 
   # for every username recieved from client input:
   #   add user to list of usernames
   # clientSocket.send(chatroom_name)

   #cmd_queue = queue.Queue()
#stdout_lock = threading.Lock()
#dj = threading.Thread(target=console, args=(cmd_queue, ))
#dj.start()


#general
#cmd_queue = queue.Queue()
#stdout_lock = threading.Lock()
#dj = threading.Thread(target=console, args=(cmd_queue, ))
#dj.start()

#print("To load a chatroom: type load_chatroom_client; To send a message: type send_message_client; To create a chatroom: type create_chatroom_client \n")
    #print("To add a user: type add_user_client; to delete a user: type delete_user_client")
    
    #user_input = input("To continue, please enter one of the following commands below, type q to quit. \n")
    
    #cmd = cmd_queue.get()

