from __future__ import print_function

import base64
import json
import logging

import cv2
import face_recognition
import grpc
import numpy as np

import cctv_stream_pb2
import cctv_stream_pb2_grpc
from core.face_recognition_lib import face_identification


def face_recognition_v1(stub):
    response = stub.SendFrame(cctv_stream_pb2.Request())
    while True:
        data = base64.b64decode(response.data)
        frame = np.frombuffer(data, dtype=np.uint8).reshape(response.width, response.high, response.ch)
        face_identification(frame, known_face_encodings, known_face_names)


def face_recognition_stream(stub):
    print("face_recognition_stream started")
    responses = stub.SendFrameStream(cctv_stream_pb2.Request())
    for response in responses:
        data = base64.b64decode(response.data)
        frame = np.frombuffer(data, dtype=np.uint8).reshape(response.width, response.high, response.ch)
        face_identification(frame, known_face_encodings, known_face_names)
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break

def run():
    with grpc.insecure_channel('localhost:52021') as channel:
        stub = cctv_stream_pb2_grpc.CCTVStreamStub(channel)
        # face_recognition_v1(stub)
        face_recognition_stream(stub)
    
    

if __name__ == '__main__':
    logging.basicConfig()
    obama_image = face_recognition.load_image_file("obama.png")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    biden_image = face_recognition.load_image_file("biden.jpeg")
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    jihar_image = face_recognition.load_image_file("jihar.jpg")
    jihar_face_encoding = face_recognition.face_encodings(jihar_image)[0]

    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding,
        jihar_face_encoding,
    ]
    known_face_names = [
        "Barack Obama",
        "Joe Biden",
        "Jihar",
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    run()
