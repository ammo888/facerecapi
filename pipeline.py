"""Pipeline takes an input image, passes it through the API, and displays and image
with the detected faces and users drawn"""
import io
import sys
import requests
from PIL import Image, ImageDraw


def main():
    """Face detection to API pipeline"""

    # Get image path and name
    ipport = sys.argv[1]
    imagepath = sys.argv[2]
    imname = imagepath.split('/')[-1]

    # Convert image to bytes
    image = Image.open(imagepath)
    imbytes = io.BytesIO()
    image.save(imbytes, format='jpeg')

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
        drawinfo(image, face['location'], face['name'])
    image.show()

def drawinfo(image, locs, text):
    """Draws rectangle around face and prints user name next to it.
    Includes a black border around text for visibility."""

    draw = ImageDraw.Draw(image)
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
