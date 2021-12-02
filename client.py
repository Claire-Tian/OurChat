#import structure

# def add_user_client():
#   sentence = input("Enter users to add!")
#   while sentence != 'q':
#       clientSocket.send(sentence)
#       # server-side code
#       # Check userID in users hash table 
#       # if it's not, raise an error in. 
#       # Otherwise, add new user to “users” list in chatID in chats hashtable (if user not already in chat)
#       # server sends confirmation message back to the client.
#       response = clientSocket.recv(1024) 
#       print ('From Server:'), response

# def delete_user_client(): 
#   user = input("Enter user to delete!")
#   clientSocket.send(user)
#   # server side code deletes user 
#   message = clientSocket.recv(1024) 
#   print ('From Server:'), message

# def load_chatroom_client(): 
#   chatroom_name = input("Enter the chatroom name")
#   clientSocket.send(chatroom_name)
#   # server side code, returns chatroom
#   message = clientSocket.recv(1024) 
#   print ('From Server:'), message

#def create_chatroom_client():
   # usernames = []
   # for every username recieved from client input:
   #   add user to list of usernames
   # clientSocket.send(chatroom_name)
   # message = clientSocket.recv(1024) 
   # print ('From Server:'), message

#def get_my_chats():
  #sent back a list of chatrooms from server, which are displayed in terminal
