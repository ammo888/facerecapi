import io
import cv2
import time
import requests
from PIL import Image
import face_recognition

def main():
    video_capture = cv2.VideoCapture(0)
    framecount = 0
    while True:
        framecount += 1
        time.sleep(3)        
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        im = Image.fromarray(small_frame)        
        im.show()
        locs = face_recognition.face_locations(small_frame)
        print('Frame', framecount)
        if locs:
            for loc in locs:
                face = im.crop((loc[3], loc[0], loc[1], loc[2]))
#                face.show()
                facebytes = io.BytesIO()
                face.save(facebytes, format='JPEG')
                auth = ('admin', 'adminadmin')
                data = {'name': ''}
                files = {'image': ('frame', facebytes.getvalue())}
                resp = requests.post('http://127.0.0.1:8000/imagebank/, auth=auth, data=data, files=files')
                print(resp.json())
        print()

if __name__ == '__main__':
    main()

