from enum import Enum


class ImageChoices:
    class DallEModel(Enum):
        dall_e_3 = 1
        dall_e_2 = 2

    class ImageSize(Enum):
        size_256x256 = 1
        size_512x512 = 2
        size_1024x1024 = 3
        size_1792x1024 = 4
        size_1024x1792 = 5

    class ImageQuality(Enum):
        standard = 1
        hd = 1
