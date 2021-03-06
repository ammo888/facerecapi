"""Definition for Faces class that handles the face recognition
part of the API"""
import os
import io
import time
import pickle
import hashlib
import sqlite3
import threading
import requests
import numpy as np
from PIL import Image
from scipy import spatial

import face_recognition


class Faces(object):
    """Class that handles identifying faces in input images and updating
    the user database."""

    def __init__(self):
        # Open .pickle files - our database
        self.database = 'database/'
        with open(os.path.join(self.database, 'hash.pickle'), 'rb') as handle:
            self.hashes = pickle.load(handle)
        with open(os.path.join(self.database, 'data.pickle'), 'rb') as handle:
            self.embeddings = pickle.load(handle)

        # cKDTree is used for finding nearest embedding by L2 norm
        # Only create tree if database isn't empty
        if self.embeddings:
            self.tree = spatial.cKDTree(self.embeddings, leafsize=100)

        # The *currently* arbitrary threshold of embedding similarity
        self.threshold = 0.5

        # API endpoint for retreiving images
        self.imagebank = 'http://127.0.0.1:8000/imagebank/'

        # User database
        self.conn = sqlite3.connect('users.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def identify(self, post_id):
        """Identify input face using the database"""

        # Fetch raw data from API endpoint
        data = requests.get(self.imagebank + str(post_id) + '/data/', stream=True)
        # Convert to numpy array
        array = np.array(Image.open(io.BytesIO(data.raw.read())))
        # Obtain face embedding
        locs = face_recognition.face_locations(array)
        embeddings = face_recognition.face_encodings(array, locs)

        rtn = []

        keys = ('name', 'gender', 'distance', 'location')
        # If embeddings are found
        if embeddings:
            for i, embedding in enumerate(embeddings):
                # Find nearest embedding in database, assuming database isn't empty
                if hasattr(self, 'tree'):
                    dist, index = self.tree.query(embedding)
                else:
                    dist, index = self.threshold, 0

                no_face = ('Face not in database', None, None, locs[i])
                # If that embedding is close enough, access user db by hash
                if dist < self.threshold:
                    # Obtain user hash
                    user_hash = (self.hashes[index],)
                    # SQL fetch user data
                    self.cursor.execute('SELECT name, gender FROM users WHERE hash=?', user_hash)
                    user_data = self.cursor.fetchone()
                    if user_data:
                        rtn.append(dict(zip(keys, user_data + (dist,) + (locs[i],))))
                    else:
                        rtn.append(dict(zip(keys, no_face)))
                else:
                    rtn.append(dict(zip(keys, no_face)))
        # No face found in image
        else:
            rtn.append('No face found')

        return rtn

    def update(self, post_id):
        """Add/update face to database"""

        # Fetch name and data from API endpoints
        user_data = requests.get(self.imagebank + str(post_id) + '/').json()
        name = user_data['name']
        gender = user_data['gender']
        data = requests.get(self.imagebank + str(post_id) + '/data/', stream=True)

        # User data hash
        user_hash = hashlib.sha256()
        user_hash.update(name.encode('utf-8'))
        user_hash.update(gender.encode('utf-8'))
        hash_str = user_hash.hexdigest()

        # Convert to numpy array
        array = np.array(Image.open(io.BytesIO(data.raw.read())))
        # Obtain face embedding
        embedding = face_recognition.face_encodings(array)

        # If embedding is found
        if embedding:
            # Find user if hash already in database
            if hash_str in self.hashes:
                # Find index
                index = self.hashes.index(hash_str)
                # Update existing user embedding
                self.embeddings[index] = embedding[0]
                # Recreate cKDTree
                self.tree = spatial.cKDTree(self.embeddings)

                rtn = [' '.join(('Updated', hash_str, 'embedding'))]
            # Name not in database
            else:
                # Add hasb and data to database
                self.hashes.append(hash_str)
                self.embeddings.append(embedding[0])
                # Recreate cKDTree
                self.tree = spatial.cKDTree(self.embeddings)

                # Add user to user db
                user_info = (hash_str, name, gender)
                self.cursor.execute('INSERT INTO users VALUES (?,?,?)', user_info)
                self.conn.commit()

                rtn = [' '.join(('Added', hash_str, 'embedding'))]

        # No face found in image
        else:
            rtn = ['No face found']

        return rtn

    def save(self):
        """Periodically pickle current database and save"""

        threading.Timer(10, self.save).start()
        with open(os.path.join(self.database, 'hash.pickle'), 'wb') as handle:
            pickle.dump(self.hashes, handle, protocol=2)

        with open(os.path.join(self.database, 'data.pickle'), 'wb') as handle:
            pickle.dump(self.embeddings, handle, protocol=2)

        now = time.strftime('[%d/%b/%Y %H:%M:%S]')
        print(now, 'Database saved')
