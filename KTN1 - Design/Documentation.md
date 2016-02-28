# Client.py

## Functions

* **run()** - Handles logic at runtime, this includes taking input from the user and parsing the input into the send_payload() method in the client object. This function also prints out a short message at startup with information about the client.

## Variables

* **client** - The client object created at startup. 
* **message_parser** - A MessageParser object.

## Classes

### Client

Handles client logic

##### Variables

* **connection** - The connection to the server.
* **server_port** - The port on the server for the connection.
* **host** - The host address of the server.

##### Methods

* **\_\_init\_\_(self, host, server_port)** - Setup connection variables and calls run method for connecting the client to the server
* **disconnect(self)** - Handles log out and disconnect from server, stops all the MessageReceiver thread.
* **run(self)** - Connects the client to the server, starts a MessageReceiver thread for receiving messages from the server. 
* **send\_payload(self, data)** - Handles sending of requests from client to server

# MessageReceiver.py

## Classes

### MessageReceiver

Handles message receiving

##### Variables

* **client** - The Client object
* **connection** - The connection to the server
* **message_parser** - A MessageParser object.

##### Methods

* **\_\_init\_\_(self, client, connection)** - Creates a MessageReceiver object
* **run(self)** - Listens to the connection for incoming messages from the server. Sends all messages to the parse() method in the MessageParser object. 

# MessageParser.py

## Functions

* **print\_formatted\_message(timestamp, sender, response_type, contentr)** - Prints formatted message/error to the console.

## Classes

### MessageParser

Encodes, decodes and parses messages

##### Methods

* **\_\_init\_\_(self)** - Creates a MessageParser object with a dictionary for response codes
* **parse(self, payload)** - Parses and handles the json payload
* **encode(self, request, content)** - Encodes request and content to json string.
* **parse_error(self, payload)** - Handles a error response and prints the error message using print\_formatted\_message()
* **parse_info(self, payload)** - Handles a info response and prints the info message using print\_formatted\_message()
* **parse_message(self, payload)** - Handles a message response and prints the message using print\_formatted\_message()
* **parse_history(self, payload)** - Handles a history response, calls parse_message() for each message

# Server.py

Contains all server logic

## Variables

* **history** - List containing message objects for all messages sent while server was running
* **users** - Dictionary with username as key and ClientHandler object for all users who have logged in.
* **unlogged_users** - List of all clients that have not logged in.

## Functions

* **username_available(username)** - Returns True if the username is free, returns False if username is taken. 
* **valid_username(username)** - Returns True if the username is in the format [A-z0-9]+
* **parse_request(payload, user)** - Parses the json object and calls on another function for handling the request. Checks if user is logged in, if not limits user commands to help and login.
* **parse_login(payload, user)** - Checks if the user is logged in, username is in wrong format or username is taken and sends error message if necessary, if not register user and send info response. Sends any message history the server has
* **parse_logout(user)** - Disconnects the user, removes user from user dictionary
* **parse_message(payload, user)** - Saves message object and sends message to all other users logged in to the server
* **parse_help(user)** - Sends a response to the user with a help text
* **parse_names(user)** - Sends the user a response of all logged in users

## Classes

### ThreadedTCPServer

Creates threads for server

* Builds on the **socketserver** packet and will not be changed.

### ClientHandler

Handles connection between server and client

##### Variables

* **ip** - IP address of client
* **port** - Client port
* **connection** - Connection between client and server

##### Methods

* **handle(self)** - Setup a connection between the client and server and waits for messages from client
* **close(self)** - Closes connection between the client and server
* **send(self, payload)** - Sends a message to the client, encodes the payload (From JSON to string)

# Message.py

## Classes

### Message

Creates message objects, used for history

##### Variables

* **message\_text** - String with text content of the message
* **user** - String for username of message sender
* **timestamp** - String with timestamp of message received at server

##### Methods

* **\_\_init\_\_(self, message\_text, username, timestamp)** - Creates a message object containing message text, user and timestamp
* **get\_message\_text(self)** - Returns message text
* **get\_user(self)** - Returns username for the sender of the message
* **get\_timestamp(self)** - Returns timestamp for the message
* **to_JSON(self)** - Returns a json response in the server response format with timestamp as original timestamp for message, sender as user, response as "Message" and content as message text