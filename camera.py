import sys
import cv2
import requests
import face_recognition


def main():
    ipport = sys.argv[1]
    video_capture = cv2.VideoCapture(0)

    framecount = 0
    while True:
        framecount += 1
        _, frame = video_capture.read()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        locs = face_recognition.face_locations(frame)

        print('Frame', framecount)
        if locs:
            for (top, right, bottom, left) in locs:
                face = frame[top:bottom, left:right]
                facebytes = bytearray(cv2.imencode('.jpg', face)[1].tostring())
                auth = ('admin', 'adminadmin')
                data = {'name': ''}
                files = {'image': ('frame', facebytes)}
                resp = requests.post(
                    'http://' + ipport + '/imagebank/', auth=auth, data=data, files=files)
                print(resp.json())
        print()      

if __name__ == '__main__':
    main()
