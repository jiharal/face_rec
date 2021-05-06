import logging
import time
from concurrent import futures

import cv2
import grpc
import numpy as np

import cctv_stream_pb2
import cctv_stream_pb2_grpc


class CCTVStream(cctv_stream_pb2_grpc.CCTVStreamServicer):
    def SendFrame(self, request, context):
        video_capture = cv2.VideoCapture(0)
        time.sleep(1)
        ret, frame = video_capture.read()
        if ret:
            print(type(frame))
            resp = np.array_str(frame, sep=',')
            cv2.imwrite('data/img{}.jpg'.format(time.time()),frame)
            print(type(resp))
            print(resp)
            return cctv_stream_pb2.Response(data=resp)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cctv_stream_pb2_grpc.add_CCTVStreamServicer_to_server(CCTVStream(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
