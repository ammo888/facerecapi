import os
import sys
import pickle

# Obtain image folder path
fpath = sys.argv[1]

hashes = []
embeddings = []

# Pickle database and save
with open(os.path.join(fpath, 'hash.pickle'), 'wb') as handle:
    pickle.dump(hashes, handle, protocol=2)

with open(os.path.join(fpath, 'data.pickle'), 'wb') as handle:
    pickle.dump(embeddings, handle, protocol=2)
