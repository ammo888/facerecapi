import sys
import cv2
import requests
from PIL import Image
import face_recognition


def main():
    ipport = sys.argv[1]
    video_capture = cv2.VideoCapture(0)

    framecount = 0
    while framecount < 30:
        framecount += 1
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        locs = face_recognition.face_locations(small_frame)

        font = cv2.FONT_HERSHEY_DUPLEX
        print('Frame', framecount)
        if locs:
            for (top, right, bottom, left) in locs:
                face = small_frame[top:bottom, left:right]
                facebytes = bytearray(cv2.imencode('.jpg', face)[1].tostring())
                auth = ('admin', 'adminadmin')
                data = {'name': '', 'gender': ''}
                files = {'image': ('frame', facebytes)}
                resp = requests.post(
                    'http://' + ipport + '/imagebank/', auth=auth, data=data, files=files)
                print(resp.json())
            
                cv2.rectangle(frame, (4*left, 4*top), (4*right, 4*bottom), (255,0,0), 2)
                if type(resp.json()) is dict:
                    cv2.putText(frame, resp.json()['name'], (4*left+6, 4*bottom-6), font, 1.0, (255,255,255), 1)
                else:
                    cv2.putText(frame, resp.json()[0], (4*left+6, 4*bottom-6), font, 1.0, (255,255,255), 1)
        print()
        im = Image.fromarray(frame)
        im.show()
    
    video_capture.release()

if __name__ == '__main__':
    main()
