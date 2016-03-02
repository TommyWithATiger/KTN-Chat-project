import socket
import json
from time import sleep

clients = []
client_names = ["client0", "client1", "client2", "client3", "client4", "client5", "client6", "client7", "client8", "client9", "testUser"]


class Client:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('localhost', 9998))
        self.client.settimeout(1)
        self.name = name

    def get_name(self):
        return self.name

    def send(self, request, content):
        self.client.send(json.dumps({
            'request': request,
            'content': content
        }).encode("UTF-8"))

    def print_recieved(self):
        try:
            received = json.loads(self.client.recv(4096).decode())
            print(received['timestamp'])
            print(received['sender'])
            print(received['response'])
            print(received['content'] + "\n")
        except TimeoutError:
            print("Server did not return anything")

    def print_recieved_history(self):
        try:
            received = json.loads(self.client.recv(4096).decode())
            print(received['timestamp'])
            print(received['sender'])
            print(received['response'])
            print(received['content'])
            for message in received['content']:
                print(message['timestamp'], message['sender'], message['content'])
            print("\n")
        except TimeoutError:
            print("Server did not return anything")

    def get_recieved_content(self):
        try:
            return json.loads(self.client.recv(4096).decode())['content']
        except TimeoutError:
            return "Server did not return anything"

for i in range(10):
    client = Client("client" + str(i))
    client.send('login', client.name)
    if client.get_recieved_content() == 'Login successful!':
        print("Client" + str(i) + " logged in successful")
    else:
        print("Client" + str(i) + " did not log in successful")
    clients.append(client)
    client.send('msg', 'test message ' + str(i + 1))

client = Client("testUser")
client.send("help", "")
client.print_recieved()
sleep(0.05)
client.send("msg", "Test message")
client.print_recieved()
sleep(0.05)
client.send("login", "")
client.print_recieved()
sleep(0.05)
client.send("login", "testUser")
client.print_recieved()
client.print_recieved_history()
sleep(0.05)
client.send("msg", "test")
sleep(0.05)
client.send("names", "")
client.print_recieved()
sleep(0.05)

for client2 in clients:
    client2.send("logout", "")
    client_names = client_names[1:]
    client.send("names", "")
    for client_name in client.get_recieved_content().split(", "):
        if client_name not in client_names:
            print(client2.get_name() + " did not logout successful")
            break
    else:
        print(client2.get_name() + " logged out successful")
    sleep(0.05)

client.send("logout", "")