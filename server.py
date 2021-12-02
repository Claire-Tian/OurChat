#import structure.py 

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

#def load_chatroom_server():
  #get corresponding chat_id from chat_name in Chatnames dictionary
  #search for chat_id in Chats hash table
  #get last_pushed_time of this user
  #send_message(chat history + time stamp) 
  #send confirmation message back to client (UI?)
#def send_message(message):
  # Get current chat_id of client (sent by client or retrieved in another way)?
  # Add “client_id, time_stamp = now, message” to history field in chat_id
  # Push all unread messages to all active users in the chat, change their last_pushed_time to now

#def get_my_chats:
  #Get user_id of client
  #Print content of “chats” field for this user in Users hashtable
