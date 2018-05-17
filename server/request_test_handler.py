import sys

import cv2
from multipledispatch import dispatch

import server
from file_path_manager import FilePathManager
from misc.connection_helper import ConnectionHelper
from misc.image_helper import ImageHelper
from server.message.add_person_message import AddPersonMessage
from server.message.close_message import CloseMessage
from server.message.end_add_person_message import EndAddPersonMessage
from server.message.face_recognition_message import FaceRecognitionMessage
from server.message.image_message import ImageMessage
from server.message.image_to_text_message import ImageToTextMessage
from server.message.register_face_recognition_message import RegisterFaceRecognitionMessage
from server.message.remove_person_message import RemovePersonMessage
from server.message.start_face_recognition_message import StartFaceRecognitionMessage
from server.message.vqa_message import VqaMessage

sys.modules['skill-socket_ITE-5th'] = server


class RequestHandler:
    def __init__(self):
        self.face_recognition = None
        self.images = []
        self.base_path = FilePathManager.resolve("saved_images")

    @dispatch(RegisterFaceRecognitionMessage)
    def handle_message(self, message):
        result = {"result": message.name, "registered": True}
        # FaceRecognitionModel.register(message.name, remove_dir=False)
        return result

    @dispatch(StartFaceRecognitionMessage)
    def handle_message(self, message):
        result = {"result": "success"}
        return result

    @dispatch(AddPersonMessage)
    def handle_message(self, message):
        result = {

        }
        cv2.imwrite(f"{self.base_path}/image_{len(self.images) + 1}.jpg", message.image)
        self.images.append(message.image)
        result["result"] = "success"
        return result

    @dispatch(EndAddPersonMessage)
    def handle_message(self, message):
        result = {"result": "success"}
        return result

    @dispatch(RemovePersonMessage)
    def handle_message(self, message):
        result = {"result": "success"}
        return result

    @dispatch(FaceRecognitionMessage)
    def handle_message(self, message):
        result = {"result": "FaceRecognitionMessage"}
        return result

    @dispatch(VqaMessage)
    def handle_message(self, message):
        result = {"result": "Visual Question Answering"}
        return result

    @dispatch(ImageToTextMessage)
    def handle_message(self, message):
        result = {"result": "image to text"}
        return result

    def start(self, client_socket):
        try:
            while True:
                message = ConnectionHelper.receive_pickle(client_socket)
                if isinstance(message, CloseMessage):
                    break
                if isinstance(message, ImageMessage):
                    message.image = ImageHelper.to_image(message.image)
                result = self.handle_message(message)
                ConnectionHelper.send_json(client_socket, result)
                print("result:")
                print(result)
        finally:
            print("socket closed")
            client_socket.close()
