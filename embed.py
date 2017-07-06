import face_recognition
import argparse
import os
import numpy as np
import pickle


parser = argparse.ArgumentParser(description='Argument Parser')
parser.add_argument('infolder',
                    help='folder that contains labelled folders of faces')
parser.add_argument('outfolder',
                    help='folder to store embeddings')
parser.add_argument('-v', '--verbose',
                    help='increase output verbosity', action='store_true')
args = parser.parse_args()

fpath = args.infolder
im_total = 1000
names = []
embeddings = []
for i, npath in enumerate(os.listdir(fpath)):
    if i == im_total:
        break
    embedding = np.zeros((128,))
    num_im = 0

    for ipath in os.listdir(os.path.join(fpath, npath)):
        face_image = face_recognition.load_image_file(
            os.path.join(fpath, npath, ipath))
        face_embedding = face_recognition.face_encodings(face_image)
        if face_embedding:
            embedding = np.add(embedding, face_embedding[0])
            num_im += 1
    if num_im > 0:
        embedding = np.divide(embedding, num_im)
        embeddings.append(embedding)
        names.append(npath)
        print('Embedded', npath)
    else:
        print('Not embedded', npath)

with open(os.path.join(args.outfolder, 'names.pickle'), 'wb') as handle:
    pickle.dump(names, handle, protocol=2)

with open(os.path.join(args.outfolder, 'data.pickle'), 'wb') as handle:
    pickle.dump(embeddings, handle, protocol=2)
