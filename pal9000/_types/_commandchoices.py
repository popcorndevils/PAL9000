from enum import Enum


class ImageCommandChoices:
    class DallEModel(Enum):
        dall_e_3 = "dall-e-3"
        dall_e_2 = 'dall-e-2'

    class ImageSize(Enum):
        size_256x256 = "256x256"
        size_512x512 = "512x512"
        size_1024x1024 = "1024x1024"
        size_1792x1024 = "1792x1024"
        size_1024x1792 = "1024x1792"

    class ImageQuality(Enum):
        standard = "standard"
        hd = "hd"


class ChatGptChoices:
    class ChatModel(Enum):
        GPT_3_5_Turbo = "gpt-3.5-turbo"
        GPT_4 = "gpt-4"
