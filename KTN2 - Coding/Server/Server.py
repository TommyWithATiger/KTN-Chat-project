# -*- coding: utf-8 -*-
import socketserver
import re
import json
import datetime
import Message


def username_available(username):
    return username not in users.values()


def valid_username(username):
    return re.match("[A-Za-z0-9]+", username) == username


def user_logged_in(user):
    return user in users.keys()


def get_username(user):
    for client, username in users.items():
        if client == user:
            return username
    return ""


def current_timestamp():
    time = datetime.datetime.now()
    timestamp = "0" * (time.month < 10) + str(time.month) + "." + "0" * (time.day < 10) + str(time.day) + " "
    timestamp += "0" * (time.hour < 10) + str(time.hour) + ":" + "0" * (time.minute < 10) + str(
            time.minute) + ":" + "0" * (time.second < 10) + str(time.second)
    return timestamp


def encode(sender, response, content):
    json_object = {
        'timestamp': current_timestamp(),
        'sender': sender,
        'response': response,
        'content': content
    }
    return json.dumps(json_object, separators=(',', ':'))


def parse_request(payload, user):
    payload = json.loads(payload)
    if not user_logged_in(user) and payload['request'] not in ['help', 'login']:
        user.send(encode("server", "error", "Please login to get access to that command, use 'help' for login help"))
    if payload['request'] in request_codes.keys():
        request_codes[payload['request']](payload['content'], user)
    else:
        user.send(encode("server", "error",
                         "Request not supported by the server, use 'help' for a list of supported requests"))


def parse_login(username, user):
    if user_logged_in(user):
        user.send(encode("server", "error", "Username already taken"))
        return
    if not valid_username(username):
        user.send(encode("server", "error",
                         "Username not valid, username has to be capital/lowercase letters and/or numbers"))
        return
    if not username_available(username):
        user.send(encode("server", "error", "Username taken"))
        return
    users[user] = username
    user.send(encode("server", "info", "Login successful!"))
    history_json = []
    for message in history:
        history_json.append(json.load(message.to_JSON))
    user.send(encode("server", "history", history_json))


def parse_logout(content, user):
    if user_logged_in(user):
        users.pop(get_username(user))
    else:
        unlogged_users.remove(user)
    user.close()


def parse_message(message, user):
    message = Message(message, get_username(user), current_timestamp())
    history.append(message)
    message_JSON = message.to_JSON
    for client in users.values():
        if client != user:
            client.send_payload(message_JSON)


def parse_help(content, user):
    help_message = "Supported requests are: \n " \
                   "login <username> - Login to the server with the specified username \n" \
                   "logout - Log out and disconnect from the server \n" \
                   "msg <message> - Sends the specified message to all connected users \n" \
                   "names - A list of the username of all connected users \n" \
                   "help - Shows all requests supported by the server"
    user.send(encode("server", "info", help_message))


def parse_names(content, user):
    username_list = ""
    for username in users.keys():
        username_list += username + ", "
    if len(username_list) != 0:
        username_list = username_list[0:-2]
    else:
        username_list = "No users logged in"
    user.send(encode("server", "info", username_list))


history = []
users = {}
unlogged_users = []
request_codes = {
    'login': parse_login,
    'logout': parse_logout,
    'msg': parse_message,
    'help': parse_help,
    'names': parse_names
}


class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)

            # TODO: Add handling of received payload from client


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True


if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
