import io
import sys
import requests
import numpy as np
from PIL import Image, ImageDraw

import face_recognition


def main():
    """Face detection to API pipeline"""

    # Get image path and name
    ipport = sys.argv[1]
    imagepath = sys.argv[2]
    imname = imagepath.split('/')[-1]

    # Convert image to bytes
    im = Image.open(imagepath)
    imbytes = io.BytesIO()
    im.save(imbytes, format='jpeg')

    # Send a HTTP POST request and print response
    auth = ('admin', 'adminadmin')
    data = {'name': ''}
    files = {'image': (imname, imbytes.getvalue())}
    resp = requests.post(
        'http://' + ipport + '/imagebank/', auth=auth, data=data, files=files)
    print(len(resp.json()), 'faces detected')
    for face in resp.json():
        print(face)

    # Draw detected faces
    for face in resp.json():
        drawInfo(im, face['location'], face['name'])
    im.show()

def drawInfo(im, locs, text):
    draw = ImageDraw.Draw(im)
    (top, right, bottom, left) = locs
    # Bounding box
    draw.rectangle(((left, top), (right, bottom)), outline='red')
    # Black border
    draw.text((left-1, bottom-1), text, fill='black')
    draw.text((left+1, bottom-1), text, fill='black')
    draw.text((left-1, bottom+1), text, fill='black')
    draw.text((left+1, bottom+1), text, fill='black')
    # Text
    draw.text((left, bottom), text, fill='white')
    del draw

if __name__ == '__main__':
    main()
