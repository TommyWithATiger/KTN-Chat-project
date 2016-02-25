# Client.py

## Functions

* **print\_formatted\_message(message)** - Prints formatted message/error

## Classes

### Client

Handles client logic

##### Methods

* **disconnect(self)** - Handles log out and disconnect from server
* **run(self)** - Connects to client to server
* **receive\_message(self, message)** - Handles incoming message
* **send\_payload(self, payload)** - Handles sending of payload

# MessageReceiver.py

## Functions

## Classes

### MessageReceiver

Handles message receiving

##### Methods

* **\_\_init\_\_(self, client, connection)** - Creates a MessageReceiver object
* **run(self)** - Handles receiving payload

# MessageParser.py

## Functions

## Classes

### MessageParser

Code and decode json message

##### Methods

* **\_\_init\_\_(self)** - Creates a MessageParser object with a dictionary for response codes
* **parse(self, payload)** - Parses and handles the json payload
* **encode(self, payload)** - Encodes payload to json for transfer
* **parse_error(self, payload)** - Parses a error response
* **parse_info(self, payload)** - Parses a info response
* **parse_message(self, payload)** - Parses a message response
* **parse_history(self, payload)** - Takes 

# Server.py

Contains all server logic

## Variables

* **history** - List containing message objects for all messages sent while server was running
* **users** - Dictionary with username as key and ClientHandler object for all users. If user hasn't logged in yet the username is set to \*

## Functions

* **username\_available(username)** - Returns True if the username is free, returns False if username is taken. 
* **valid\_username(username)** - Returns True if the username is in the format [A-z0-9]+
* **parse\_request(payload, user)** - Parses the json object and calls on another function for handling the request
* **parse\_login(payload, user)** - Checks if the user is logged in, username is in wrong format or username is taken and sends error message if necessary, if not register user and send info response. Sends any message history the server has
* **parse\_logout(user)** - Disconnects the user, removes user from user dictionary
* **parse\_message(payload, user)** - Saves message object and sends message to all other users logged in to the server
* **parse\_help(user)** - Sends a response to the user with a help text
* **parse\_names(user)** - Sends the user a response of all logged in users
* ****

## Classes

### ThreadedTCPServer

Creates threads for server

##### Methods

* Builds on the **socketserver** packet and will not need any new methods.

### ClientHandler

Handles connection between server and client

##### Methods

* **handle(self)** - Setup a connection between the client and server and waits for messages from client
* **close(self)** - Closes connection between the client and server
* **send(self, payload)** - Sends a message to the client

# Message.py

## Classes

### Message

Creates message objects, used for history

##### Methods

* **\_\_init\_\_(self)** - Creates a message object containing message text, user and timestamp
* **get\_message(self)** - Returns message text
* **get\_user(self)** - Returns username for the sender of the message
* **get\_timestamp(self)** - Returns timestamp for the message