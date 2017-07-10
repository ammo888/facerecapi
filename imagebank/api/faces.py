import os
import io
import sys
import time
import pickle
import hashlib
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
        self.database = 'newdb/'
        with open(os.path.join(self.database, 'hash.pickle'), 'rb') as handle:
            self.hashes = pickle.load(handle)
        with open(os.path.join(self.database, 'data.pickle'), 'rb') as handle:
            self.embeddings = pickle.load(handle)

        # cKDTree is used for finding closest embedding by L2 norm
        if self.embeddings:
            self.tree = spatial.cKDTree(self.embeddings, leafsize=100)

        # The *currently* arbitrary threshold of embedding similarity
        self.threshold = 0.42

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
            if hasattr(self, 'tree'):
                dist, ind = self.tree.query(embedding[0])
            else:
                dist, ind = 10, 0
            # If that embedding is close enough, return the embedding info
            if dist < self.threshold:
                rtn = self.hashes[ind] + ' ' + str(dist)
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
        userdata = requests.get(self.imagebank + str(id) + '/').json()
        name = userdata['name']
        gender = userdata['gender']
        data = requests.get(self.imagebank + str(id) + '/data/', stream=True)

        # User hash
        userhash = hashlib.sha256()
        userhash.update(name.encode('utf-8'))
        userhash.update(gender.encode('utf-8'))
        userhash = userhash.hexdigest()

        # Convert to numpy array
        array = np.array(Image.open(io.BytesIO(data.raw.read())))
        # Obtain face embedding
        embedding = face_recognition.face_encodings(array)

        # If embedding is found
        if embedding:
            # Find user hash already in database
            if userhash in self.hashes:
                # Find index
                index = self.hashes.index(userhash)
                # Update existing embedding
                self.embeddings[index] = (
                    self.embeddings[index] + embedding[0]) / 2
                self.tree = spatial.cKDTree(self.embeddings)
                rtn = 'Updated ' + userhash + ' embedding'
            # Name not in database
            else:
                # Add hasb and data to database
                self.hashes.append(userhash)
                self.embeddings.append(embedding[0])
                # Recreate cKDTree
                self.tree = spatial.cKDTree(self.embeddings)
                rtn = 'Added ' + userhash + ' embedding'

        # No face found in image
        else:
            rtn = 'No face found'

        return rtn

    def save(self):
        """Periodically pickle current database and save"""

        # threading.Timer(10, self.save).start()
        # with open(os.path.join(self.database, 'hash.pickle'), 'wb') as handle:
        #     pickle.dump(self.hashes, handle, protocol=2)

        # with open(os.path.join(self.database, 'data.pickle'), 'wb') as handle:
        #     pickle.dump(self.embeddings, handle, protocol=2)

        now = time.strftime('[%d/%b/%Y %H:%M:%S]')
        print(now, 'Database saved')
