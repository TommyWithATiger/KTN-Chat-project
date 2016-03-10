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
        self.connection.connect((self.host, self.server_port))
        self.messagereceiver = MessageReceiver(self, self.connection)
        self.messagereceiver.start()

    def disconnect(self):
        self.messagereceiver._isAlive = False
        pass

    def send_payload(self, data):
        self.connection.send(data.encode("UTF-8"))
        pass

        # More methods may be needed!


def run():
    connected = True
    print("Welcome! Type '?' for information")
    while connected:
        text_in = input()
        if not(text_in == ""):
            if text_in[0] == "!":
                text_in = text_in[1:]
                text_in = text_in.split(" ", 1)
                if len(text_in) == 1:
                    text_in.append("")
                client.send_payload(message_parser.encode(text_in[0], text_in[1]))
                if text_in[0] == "logout":
                    connected = False
                    client.disconnect()
            elif text_in[0] == "?":
                print("How the client works:\n"
                      "Use Requests by typing '!YourRequest' 'content'\n")
            else:
                client.send_payload(message_parser.encode("msg", text_in))
        else:
            print("Write something")


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """

    client = Client("10.20.105.105", 9998)
    message_parser = MessageParser()
    run()
