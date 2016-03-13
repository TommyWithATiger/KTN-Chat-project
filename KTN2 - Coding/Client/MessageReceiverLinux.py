# -*- coding: utf-8 -*-
from threading import Thread
from MessageParserLinux import MessageParser
import socket
import json


class MessageReceiver(Thread):
    def __init__(self, client, connection):
        Thread.__init__(self)
        self.client = client
        self.connection = connection
        self.message_parser = MessageParser()
        self.is_running = True
        self.daemon = True

    def run(self):
        json_object = ""
        while self.is_running:
            try:
                received = json_object + self.connection.recv(4096).decode("UTF-8")
                try:
                    self.message_parser.parse(received)
                    json_object = ""
                except json.JSONDecodeError:
                    json_object = received
            except socket.timeout:
                print("Timeout")
                continue
            except Exception as e:
                print("Ran into an error, closing receiver: \n" + e.__str__() + "\n" + e.__traceback__)
                self.client.disconnect()
                break
