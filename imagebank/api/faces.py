import os
import io
import sys
import time
import pickle
import requests
import threading
import numpy as np
from PIL import Image
from scipy import spatial
from functools import wraps

import face_recognition


class Faces(object):

    def __init__(self):
        # Open .pickle files - our database
        self.database = 'database/'
        with open(os.path.join(self.database, 'names.pickle'), 'rb') as handle:
            self.names = pickle.load(handle)
        with open(os.path.join(self.database, 'data.pickle'), 'rb') as handle:
            self.embeddings = pickle.load(handle)

        # cKDTree is used for finding closest embedding by L2 norm
        self.tree = spatial.cKDTree(self.embeddings, leafsize=100)
        # The *currently* arbitrary threshold of embedding similarity
        self.threshold = 0.43

        # API endpoint for retreiving images
        self.imagebank = 'http://127.0.0.1:8000/imagebank/'

    def identify(self, id):
        """Identify input face using the database"""

        # Fetch raw data from API endpoint
        data = requests.get(self.imagebank + str(id) + '/data/', stream=True)
        # Convert to numpy array
        array = np.array(Image.open(io.BytesIO(data.raw.read())))
        # Obtain face embedding
        embedding = face_recognition.face_encodings(array)

        # If embedding is found
        if embedding:
            # Find nearest embedding in database
            dist, ind = self.tree.query(embedding[0])
            # If that embedding is close enough, return the embedding info
            if dist < self.threshold:
                rtn = self.names[ind] + ' ' + str(dist)
            # Else, the face is not in the database
            else:
                rtn = 'Face not in database'
        # No face found in image
        else:
            rtn = 'No face found'

        return rtn

    def update(self, id):
        """Add/update face to database"""

        # Fetch name and data from API endpoints
        name = requests.get(self.imagebank + str(id) + '/').json()['name']
        data = requests.get(self.imagebank + str(id) + '/data/', stream=True)
        # Convert to numpy array
        array = np.array(Image.open(io.BytesIO(data.raw.read())))
        # Obtain face embedding
        embedding = face_recognition.face_encodings(array)

        # If embedding is found
        if embedding:
            # Find name already in database
            if name in self.names:
                # Find index
                index = self.names.index(name)
                # Update existing embedding
                self.embeddings[index] = (
                    self.embeddings[index] + embedding[0]) / 2
                rtn = 'Updated ' + name + ' embedding'
            # Name not in database
            else:
                # Add name and data to database
                self.names.append(name)
                self.embeddings.append(embedding[0])
                # Recreate cKDTree
                self.tree = spatial.cKDTree(self.embeddings)
                rtn = 'Added ' + name + ' embedding'
        # No face found in image
        else:
            rtn = 'No face found'

        return rtn

    def save(self):
        """Periodically pickle current database and save"""

        threading.Timer(10, self.save).start()
        with open(os.path.join(self.database, 'names.pickle'), 'wb') as handle:
            pickle.dump(self.names, handle, protocol=2)

        with open(os.path.join(self.database, 'data.pickle'), 'wb') as handle:
            pickle.dump(self.embeddings, handle, protocol=2)

        now = time.strftime('[%d/%b/%Y %H:%M:%S]')
        print(now, 'Database saved')
