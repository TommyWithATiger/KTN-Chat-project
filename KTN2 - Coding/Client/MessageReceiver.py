# -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import MessageParser
import MessageParser
import socket


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """
    

    def __init__(self, client, connection):
        Thread.__init__(self)
        self.client = client
        self.connection = connection
        self.message_parser = MessageParser.MessageParser()
        #threading.Thread.__init__(self)
        #jsonSocket.JsonServer.__init__(self)
        self._isAlive = True

        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while self._isAlive:
            # try:
            #     self.acceptConnection()
            # except socket.timeout as e:
            #     logger.debug("socket.timeout: %s" % e)
            #     continue
            # except Exception as e:
            #     logger.exception(e)
            #     continue

            #while self._isAlive:
            try:
                received = self.connection.recv(4096).decode("UTF-8")
                self.message_parser.parse(received)
            except socket.timeout:
                print("Timeout")
                continue
            except Exception as e:
                print(e)
                break
