"""Camera uses the device's primary camera to capture frames,
pass the through the API, and output frames with outlined faces
and user info"""
import sys
import json
import cv2
import requests
import numpy as np
import matplotlib.pyplot as plt
import face_recognition


def main():
    """Camera to API"""
    ipport = sys.argv[1]
    video_capture = cv2.VideoCapture(0)
    width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    plt.ion()
    fig, axes = plt.subplots(figsize=(8, 4.5))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    image = axes.imshow(np.zeros((int(height), int(width), 3)))
    axes.axis('tight')
    axes.axis('off')

    framecount = 0
    while True:
        framecount += 1
        _, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        locs = face_recognition.face_locations(small_frame)
        print('\033c')
        print('Frame', framecount)
        if locs:
            for (top, right, bottom, left) in locs:
                face = small_frame[top:bottom, left:right]
                facebytes = cv2.imencode('.jpg', face)[1].tobytes()
                auth = ('admin', 'adminadmin')
                data = {'name': '', 'gender': ''}
                files = {'image': ('frame', facebytes)}
                resp = requests.post(
                    'http://' + ipport + '/imagebank/', auth=auth, data=data, files=files)

                print(json.dumps(resp.json(), indent=4))

                if resp.json() != ['No face found']:
                    cv2.rectangle(frame, (4*left, 4*top), (4*right, 4*bottom), (0, 0, 255), 2)
                    cv2.putText(frame, resp.json()[0]['name'], (4*left+6, 4*bottom-6),
                                cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 255, 0), 2)

        image.set_data(frame)
        fig.canvas.flush_events()

    video_capture.release()

if __name__ == '__main__':
    main()
