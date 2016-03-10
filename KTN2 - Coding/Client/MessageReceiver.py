# -*- coding: utf-8 -*-
from threading import Thread


class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """
    

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        threading.Thread.__init__(self)
        jsonSocket.JsonServer.__init__(self)
        self._isAlive = False

        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        while self._isAlive:
            try:
                self.acceptConnection()
            except socket.timeout as e:
                logger.debug("socket.timeout: %s" % e)
                continue
            except Exception as e:
                logger.exception(e)
                continue
 
            while self._isAlive:
                try:
                    obj = self.readObj()
                    self._processMessage(obj)
                except socket.timeout as e:
                    logger.debug("socket.timeout: %s" % e)
                    continue
                except Exception as e:
                    logger.exception(e)
                    self._closeConnection()
                    break

        pass
