import _pickle as pickle
import json


class Sender:

    def __init__(self, socket, json=True):
        self.socket = socket

        if json:
            self.send = self.send_json
        else:
            self.send = self.send_pickle

    def send(self, data):
        pass

    def send_json(self, data):
        # try:
        if '__dict__' in data:
            serialized = json.dumps(data.__dict__)
        else:
            serialized = json.dumps(data)
        # except (TypeError, ValueError) as e:
        #     raise Exception('You can only send JSON-serializable data')
        # send the length of the serialized data first
        self.socket.send((str(len(serialized)) + '\n').encode())
        # send the serialized data
        self.socket.sendall(serialized.encode())

    def send_pickle(self, object):
        try:
            serialized = pickle.dumps(object)
        except (TypeError, ValueError) as e:
            raise Exception('You can only send JSON-serializable data')
        # send the length of the serialized data first
        self.socket.send((str(len(serialized)) + '\n').encode())
        # send the serialized data
        self.socket.sendall(serialized)
