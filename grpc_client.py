from __future__ import print_function

import json
import logging

import cv2
import grpc
import numpy as np

import cctv_stream_pb2
import cctv_stream_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = cctv_stream_pb2_grpc.CCTVStreamStub(channel)
        response = stub.SendFrame(cctv_stream_pb2.Request())
    
    data = np.array([[np.uint8(j) for j in i.split('\t')] for i in response.data.splitlines()])
    print(data)
    # print(data.shape)
    # cv2.imshow("winname", response.data)
    # cv2.waitKey(0)

    print("Greeter client received:")

if __name__ == '__main__':
    logging.basicConfig()
    while True:
      run()
