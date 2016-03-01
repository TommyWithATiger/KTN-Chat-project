import json


class Message:
    def __init__(self, text, user, timestamp):
        self.message_text = text
        self.user = user
        self.timestamp = timestamp

    def to_JSON(self):
        return json.dumps({
            'timestamp': self.timestamp,
            'sender': self.user,
            'response': "message",
            'content': self.message_text
        })
