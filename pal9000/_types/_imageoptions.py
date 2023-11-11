from ._commandchoices import ImageCommandChoices


class ImageOptions:
    def __init__(self,
                 model: ImageCommandChoices.DallEModel,
                 quality: ImageCommandChoices.ImageQuality,
                 size: ImageCommandChoices.ImageSize,
                 n: int):
        self.model = model
        self.quality = quality
        self.size = size
        self.n = n

    def to_data(self):
        return {
            "model": self.model.value,
            "size": self.size.value,
            "n": self.n,
            "quality": self.quality.value,
        }
