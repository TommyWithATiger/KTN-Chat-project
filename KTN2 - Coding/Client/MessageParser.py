import json

def print_formatted_message(timestamp, response_type, content):
    print(timestamp, response_type, content)


# Pointless comment.

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload)

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print_formatted_message(payload['timestamp'], "error", "Recieved impossible response")

    def parse_error(self, payload):
        print_formatted_message(payload['timestamp'], payload['response'], payload['content'])

    def parse_info(self, payload):
        print_formatted_message(payload['timestamp'], payload['response'], payload['content'])

    def parse_message(self, payload):
        print_formatted_message(payload['timestamp'], payload['response'], payload['content'])

    def encode(self, request, content):
        encoded = json.dumps({"request": request , "content": content})
        return encoded

    def parse_history(self, payload):
        payload = payload['history']
        for i in payload.items():
            print_formatted_message(payload[i]['timestamp'], payload[i]['repsonse'], payload[i]['content'])
