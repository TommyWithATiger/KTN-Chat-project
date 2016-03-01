import socket
import json


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 9998))
client.settimeout(1)


def send(request, content):
    client.send(json.dumps({
        'request': request,
        'content': content
    }).encode("UTF-8"))


def print_recieved():
    received = json.loads(client.recv(4096).decode())
    print(received['timestamp'])
    print(received['sender'])
    print(received['response'])
    print(received['content'] + "\n")


def print_recieved2():
    received = json.loads(client.recv(4096).decode())
    print(received['timestamp'])
    print(received['sender'])
    print(received['response'])
    print(received['content'])
    for message in received['content']:
        print(message['timestamp'], message['sender'], message['content'])
    print("\n")

send("help", "")
print_recieved()

send("msg", "test")
print_recieved()

send("login", "fssdaaes")
print_recieved()
try:
    print_recieved2()
except:
    pass


send("msg", "test")


send("names", "")
print_recieved()

send("logout", "")