import io
import sys
import requests
import numpy as np
from PIL import Image

import face_recognition


def main():
    """Face detection to API pipeline"""

    # Get image path
    ipport = sys.argv[1]
    imagepath = sys.argv[2]
    # Get image name
    im_name = imagepath.split('/')[-1]

    # Obtain face locations
    im = Image.open(imagepath)
    locs = face_recognition.face_locations(np.array(im))
    print(len(locs), 'faces detected')
    # If any faces found
    if locs:
        # Go through each face
        for loc in locs:
            # Crop face
            face = im.crop((loc[3], loc[0], loc[1], loc[2]))
            # Get bytes from face image
            facebytes = io.BytesIO()
            face.save(facebytes, format='JPEG')
            # Send a HTTP POST request and print response
            data = {'name': ''}
            files = {'image': (im_name, facebytes.getvalue())}
            auth = ('admin', 'adminadmin')
            resp = requests.post(
                'http://' + ipport + '/imagebank/', auth=auth, data=data, files=files)
            print(resp.json())

if __name__ == '__main__':
    main()
