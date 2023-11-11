from ._chatlogs import ChatLogs
from ._chatmessage import ChatMessage, Roles


ChatProfiles = {
    "default": ChatLogs(
        ChatMessage(Roles.system, "You are a helpful assistant")
    )
}
