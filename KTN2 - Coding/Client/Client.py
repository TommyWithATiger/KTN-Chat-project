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
        self.messagereceiver = MessageReceiver(self, self.connection)
        self.connection.connect((self.host, self.server_port))
        
    def disconnect(self):
        self.messagereceiver.MessageReceiver(self, self.connection)
        self.connection.exit()
        pass

    def send_payload(self, data):
        self.data = data
        self.connection.send(self.data.encode("UTF-8"))
        pass
        
    # More methods may be needed!

if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
