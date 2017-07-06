import sys, io
from PIL import Image
import numpy as np
import face_recognition
import requests

def main():
    imagepath = sys.argv[1]
    im_name = imagepath.split('/')[-1]

    im = Image.open(imagepath)
    locs = face_recognition.face_locations(np.array(im))
    print(len(locs), 'faces detected')
    if locs:
        for loc in locs:
            face = im.crop((loc[3], loc[0], loc[1], loc[2]))    
            facebytes = io.BytesIO()
            face.save(facebytes, format='JPEG')
            # im.show()
            data = {'name':''}
            files = {'image': (im_name, facebytes.getvalue())}
            resp = requests.post('http://localhost:8000/imagebank/', auth=('admin', 'adminadmin'), data=data, files=files)
            print(resp.json())

if __name__ == '__main__':
    main()