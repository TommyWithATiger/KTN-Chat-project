# -*- coding: utf-8 -*-
import socket
import sys
from MessageReceiverLinux import MessageReceiver
from MessageParserLinux import MessageParser


class Client:
    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        self.connection.connect((self.host, self.server_port))
        self.messagereceiver = MessageReceiver(self, self.connection)
        self.messagereceiver.start()

    def disconnect(self):
        self.messagereceiver.is_running = False
        pass

    def send_payload(self, data):
        self.connection.send(data.encode("UTF-8"))
        pass


def run():
    connected = True
    print("Welcome! Type '?' for information")
    while connected:
        text_in = input("> ")
        if not (text_in == ""):
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
                      "Use Requests by typing '!YourRequest' 'content'\n"
                      "!logout disconnects the client from the server")
            else:
                client.send_payload(message_parser.encode("msg", text_in))
        else:
            print("\nWrite something")


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python ClientLinux.py"
    in your terminal.

    No alterations are necessary
    """

    client = Client(sys.argv[1], int(sys.argv[2]))
    message_parser = MessageParser()
    run()
