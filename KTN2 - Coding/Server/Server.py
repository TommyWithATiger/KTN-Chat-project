# -*- coding: utf-8 -*-
import socketserver
import re
import json
import time
from datetime import datetime
from Message import Message


def username_available(username):
    return username not in users.values()


def valid_username(username):
    pattern = re.compile("^[A-Za-z0-9]+$")
    return pattern.match(username)


def user_logged_in(user):
    return user in users.keys()


def get_username(user):
    if user_logged_in(user):
        return users[user]
    return ""


def current_timestamp():
    return datetime.now().strftime("%m.%d %H:%M:%S")


def encode(sender, response, content):
    return json.dumps({
        'timestamp': current_timestamp(),
        'sender': sender,
        'response': response,
        'content': content
    })


def parse_request(payload, user):
    if len(payload) == 0:
        return
    try:
        payload = json.loads(payload)
        if (not user_logged_in(user)) and payload['request'] not in ['help', 'login']:
            user.send(encode("server", "error", "Please login to get access to that command, use 'help' for login help"))
        elif payload['request'] in request_codes.keys():
            request_codes[payload['request']](payload['content'], user)
        else:
            user.send(encode("server", "error",
                             "Request not supported by the server, use 'help' for a list of supported requests"))
    except Exception as e:
        print("Exception")
        print(e.__str__())
        print(e.__traceback__)
        user.send(encode("server", "error", "Could not handle input, sending to fast, in the wrong format, in long message"))


def parse_login(username, user):
    if user_logged_in(user):
        user.send(encode("server", "error", "Username already taken"))
    elif not valid_username(username):
        user.send(encode("server", "error",
                         "Username not valid, username has to be capital/lowercase letters and/or numbers"))
    elif not username_available(username):
        user.send(encode("server", "error", "Username taken"))
    else:
        users[user] = username
        unlogged_users.remove(user)
        user.send(encode("server", "info", "Login successful!"))
        time.sleep(0.1)
        local_history = history[:]
        if len(local_history) != 0:
            history_json = []
            current_length = 200
            for message in local_history:
                current_length += len(message.to_JSON())
                history_json.append(json.loads(message.to_JSON()))
            user.send(encode("server", "history", history_json))


def parse_logout(content, user):
    if user_logged_in(user):
        users.pop(user)
    else:
        unlogged_users.remove(user)
    user.close()


def parse_message(message, user):
    if len(message) > 3796:
        user.send(encode("server", "info", "Too long message"))
        return
    message = Message(message, get_username(user), current_timestamp())
    history.append(message)
    message_JSON = message.to_JSON()
    for client in users.keys():
        if client != user:
            try:
                client.send(message_JSON)
            except ConnectionResetError:
                users.pop(client)
            except Exception as e:
                print("Exception 2")
                print(e.__str__())
                print(client.ip)
    user.send(encode("server", "info", "Message recieved"))


def parse_help(content, user):
    user.send(encode("server", "info", "Supported requests are: \n"
                                       "login <username> - Login to the server with the specified username \n"
                                       "logout - Log out and disconnect from the server \n"
                                       "msg <message> - Sends the specified message to all connected users \n"
                                       "names - A list of the username of all connected users \n"
                                       "help - Shows all requests supported by the server"))


def parse_names(content, user):
    username_list = ""
    for username in users.values():
        username_list += username + ", "
    user.send(encode("server", "info", username_list[0:-2]))


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
    def handle(self):
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.run = True
        unlogged_users.append(self)

        # Loop that listens for messages from the client
        while self.run:
            try:
                received_string = self.connection.recv(4096)
                parse_request(received_string.decode(), self)
                time.sleep(0.2)
            except ConnectionResetError:
                time.sleep(1)

    def close(self):
        self.run = False

    def send(self, payload):
        try:
            self.connection.send(payload.encode("utf-8"))
        except BrokenPipeError:
            self.close()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    HOST, PORT = '192.168.0.100', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
