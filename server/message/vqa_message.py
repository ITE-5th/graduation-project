from .image_message import ImageMessage


class VqaMessage(ImageMessage):
    def __init__(self, image=None, question=None):
        super().__init__(image)
        self.question = question
