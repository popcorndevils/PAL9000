from enum import Enum


class Roles(Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class ChatMessage:
    def __init__(self, role: Roles, msg: str):
        self.role = role
        self.msg = msg

    def to_data(self):
        return {
            "role": self.role.value,
            "content": self.msg,
        }
