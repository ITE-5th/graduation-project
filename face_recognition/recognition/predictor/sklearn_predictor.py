from joblib import load

from file_path_manager import FilePathManager
from recognition.predictor.predictor import Predictor


class SkLearnPredictor(Predictor):
    UNKNOWN = "Unknown"

    def __init__(self, model_name: str, use_cuda: bool = True, scale=1):
        super().__init__(use_cuda=use_cuda, scale=scale)
        self.model = load(FilePathManager.resolve(f"face_recognition/recognition/models/{model_name}.model"))

    def predict_from_image(self, image):
        items = super().predict_from_image(image)
        result = []
        for (face, rect) in items:
            x = face.data.cpu().numpy().reshape(1, -1)
            predicted = self.model.predict_proba(x)[0]
            clz = predicted.argmax()
            prop = predicted[clz]
            result.append((self.names[int(clz)], rect, prop))
        return result


