import os
import pickle
import argparse
import numpy as np

import face_recognition

# Parse command line arguments
parser = argparse.ArgumentParser(description='Argument Parser')
parser.add_argument('infolder',
                    help='folder that contains labelled folders of faces')
parser.add_argument('outfolder',
                    help='folder to store embeddings')
parser.add_argument('-v', '--verbose',
                    help='increase output verbosity', action='store_true')
args = parser.parse_args()

# Obtain image folder path
fpath = args.infolder
# Max number of people to embed
im_total = 1000
names = []
embeddings = []
# Go through image folder
for i, npath in enumerate(os.listdir(fpath)):
    # Stop and max number
    if i == im_total:
        break
    embedding = np.zeros((128,))
    num_im = 0
    # For every image to a person
    for ipath in os.listdir(os.path.join(fpath, npath)):
        # Obtain face embedding
        face_image = face_recognition.load_image_file(
            os.path.join(fpath, npath, ipath))
        face_embedding = face_recognition.face_encodings(face_image)
        # If face exists, add to embedding vector
        if face_embedding:
            embedding = np.add(embedding, face_embedding[0])
            num_im += 1
    # Find average face embedding for the person and add to lists
    if num_im > 0:
        embedding = np.divide(embedding, num_im)
        embeddings.append(embedding)
        names.append(npath)
        print('Embedded', npath)
    # No images/faces found
    else:
        print('Not embedded', npath)

# Pickle database and save
with open(os.path.join(args.outfolder, 'names.pickle'), 'wb') as handle:
    pickle.dump(names, handle, protocol=2)

with open(os.path.join(args.outfolder, 'data.pickle'), 'wb') as handle:
    pickle.dump(embeddings, handle, protocol=2)
