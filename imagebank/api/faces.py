import sys, os, io, time
import pickle, requests, threading
import threading
import numpy as np
from functools import wraps
from scipy import spatial
from PIL import Image
import face_recognition


class Faces(object):

    def __init__(self):
        self.database = 'database/'
        with open(os.path.join(self.database, 'names.pickle'), 'rb') as handle:
            self.names = pickle.load(handle)
        with open(os.path.join(self.database, 'data.pickle'), 'rb') as handle:
            self.embeddings = pickle.load(handle)

        self.tree = spatial.cKDTree(self.embeddings, leafsize=100)

        self.imagebank = 'http://127.0.0.1:8000/imagebank/'

    def identify(self, id):
        data = requests.get(self.imagebank + str(id) + '/data/', stream=True)
        array = np.array(Image.open(io.BytesIO(data.raw.read())))
        embedding = face_recognition.face_encodings(array)

        if embedding:
            dist, ind = self.tree.query(embedding[0])
            rtn = self.names[ind] + ' ' + str(dist)
        else:
            rtn = 'No face found'

        return rtn

    def update(self, id):
        name = requests.get(self.imagebank + str(id) + '/').json()['name']
        data = requests.get(self.imagebank + str(id) + '/data/', stream=True)
        array = np.array(Image.open(io.BytesIO(data.raw.read())))
        embedding = face_recognition.face_encodings(array)

        if embedding:
            if name in self.names:
                index = self.names.index(name)
                self.embeddings[index] = (
                    self.embeddings[index] + embedding[0]) / 2
                rtn = 'Updated ' + name + ' embedding'
            else:
                self.names.append(name)
                self.embeddings.append(embedding[0])
                self.tree = spatial.cKDTree(self.embeddings)
                rtn = 'Added ' + name + ' embedding'
        else:
            rtn = 'No face found'

        return rtn

    def save(self):
        threading.Timer(10, self.save).start()
        with open(os.path.join(self.database, 'names.pickle'), 'wb') as handle:
            pickle.dump(self.names, handle, protocol=2)

        with open(os.path.join(self.database, 'data.pickle'), 'wb') as handle:
            pickle.dump(self.embeddings, handle, protocol=2)

        now = time.strftime('[%d/%b/%Y %H:%M:%S]')
        print(now, 'Database saved')
