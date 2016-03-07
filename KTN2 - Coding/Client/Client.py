# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """This is the chat client class"""

    def __init__(self, host, server_port):
        """This method is run when creating a new Client object"""
        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        self.messagereceiver = MessageReceiver(self.connection)
        self.connection.connect((self.host, self.server_port))
        
    def disconnect(self):
        self.messagereceiver.exit()
        pass

    def send_payload(self, data):
        self.connection.send(data.encode("UTF-8"))
        pass
        
    # More methods may be needed!


def run():
    connected = True
    print("Welcome! Type '?' for information")
    while connected:
        textIn = input()
        if (textIn[0] == "!"):
            textIn = textIn[1:]
            textIn = textIn.split(" ", 1)
            message_parser.encode(textIn[0], textIn[1])
            if (textIn[0] == "logout"):
                connected = False
                client.disconnect()
        elif (textIn[0] == "?"):
            print("How the client works:/nUse Requests by typing '!YourRequest' 'content'/nAvailable requests:/nlogin <username>/nlogout/names (list users in chat)")
        else:
            message_parser.encode("msg" , textIn)

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    
    client = Client('localhost', 9998)
    message_parser = MessageParser()
    run()
    
