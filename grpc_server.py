import logging
import time
from concurrent import futures
from dotenv import load_dotenv

import cv2
import grpc
import numpy as np
import base64
import os

import cctv_stream_pb2
import cctv_stream_pb2_grpc
load_dotenv()



class CCTVStream(cctv_stream_pb2_grpc.CCTVStreamServicer):
    def SendFrame(self, request, context):
        src = os.getenv("IP_CCTV")
        if src == "0":
            src = 0
        video_capture = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = video_capture.read()
        if ret:
            resp = base64.b64encode(frame)
            return cctv_stream_pb2.Response(data=resp, width=frame.shape[0], high=frame.shape[1], ch=frame.shape[2])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cctv_stream_pb2_grpc.add_CCTVStreamServicer_to_server(CCTVStream(), server)
    addr = '[::]:{}'.format(os.getenv("PORT"))
    server.add_insecure_port(addr)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
