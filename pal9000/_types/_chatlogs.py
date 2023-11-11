from ._chatmessage import ChatMessage


class ChatLogs:
    def __init__(self, *msgs):
        self.msgs = list(msgs)

    def to_data(self):
        return [m.to_data() for m in self.msgs]

    def add_msg(self, role, msg):
        self.msgs.append(ChatMessage(role, msg))

    def __add__(self, other):
        _new = [m for m in self.msgs]
        for m in other.msgs:
            _new.append(m)
        return ChatLogs(_new)
