import os
from abc import ABCMeta, abstractmethod

import cv2
from dlt.util.misc import cv2torch
from torch.autograd import Variable

from recognition.preprocessing.aligner_preprocessor import AlignerPreprocessor
from recognition.pretrained.extractors import vgg_extractor
from file_path_manager import FilePathManager


class Predictor(metaclass=ABCMeta):
    extractor = vgg_extractor()

    def __init__(self, use_custom: bool = True, use_cuda: bool = True, scale: int = 1):
        self.use_cuda = use_cuda
        self.names = sorted(
            os.listdir(FilePathManager.resolve("face_recognition/data/{}".format("custom_images2" if use_custom else "lfw2"))))
        self.preprocessor = AlignerPreprocessor(scale)

    def predict_from_path(self, image_path: str):
        return self.predict_from_image(cv2.imread(image_path))

    @abstractmethod
    def predict_from_image(self, image):
        items = self.preprocessor.preprocess(image)
        result = []
        for (face, rect) in items:
            face = cv2.resize(face, (200, 200))
            face = cv2torch(face).float()
            face = face.unsqueeze(0)
            x = Variable(face).cuda()
            x = Predictor.extractor(x)
            result.append((x, rect))
        return result


