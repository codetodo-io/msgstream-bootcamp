# -*- coding: utf-8 -*-

import zmq
import random
import time

port = "5555"
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:%s" % port)

topics = []
# topics = ['sports.general']
if not topics:
    socket.setsockopt(zmq.SUBSCRIBE, b'')
else:
    for t in topics:
        socket.setsockopt(zmq.SUBSCRIBE, t.encode('utf-8'))

while True:
    topic, msg = socket.recv_multipart()
    print((topic, msg))
    time.sleep(1)
