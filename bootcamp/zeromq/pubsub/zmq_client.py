# -*- coding: utf-8 -*-

import zmq
import random
import time

port = "5555"
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://127.0.0.1:%s" % port)
time.sleep(1)

all_topics = [
    b'sports.general',
    b'sports.football',
    b'sports.basketball',
    b'stocks.general',
    b'stocks.GOOG',
    b'stocks.AAPL',
    b'weather',
]

for topic in all_topics:
    msg_body = str(random.randint(1, 10000))
    socket.send_multipart([topic, msg_body.encode("utf8")])
    time.sleep(0.1)
