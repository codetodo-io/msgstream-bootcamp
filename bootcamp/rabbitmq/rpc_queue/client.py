# -*- coding: utf-8 -*-

import os, pika, uuid, time, random, threading
import common

class RPCClient(object):

    def __init__(self):
        # 连接RabbitMQ并获取频道
        urls = os.environ.get('RABBITMQ_ADDRESS')
        all_endpoints = [pika.URLParameters(url) for url in urls.split(',')]
        self.connection = pika.BlockingConnection(all_endpoints)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self._results = {}
    
    def on_response(self, ch, method, props, body):
        corr_id = props.correlation_id
        if corr_id in self._results:
            self._results[corr_id] = int(body)

    def call(self, n, priority):
        self.response = None
        corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=corr_id,
                priority=priority
            ),
            body=str(n)
        )
        self._results[corr_id] = -1
        t = 3
        s_time = time.time()
        # while self._results[corr_id] == -1:
        #     if time.time() - s_time > t:
        #         break
        #     self.connection.process_data_events()
        #     time.sleep(0.001)
        self.connection.process_data_events(t)
        print(time.time() - s_time)
        return self._results.pop(corr_id)

def handle(t, priority):
    rpc = RPCClient()
    for i in range(100):
        res = rpc.call(i // 10, priority)
        time.sleep(0.5)
        print((t, priority, res))

if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=handle, args=(i, i, ))
        t.start()
        print('Thread: %d' % i)
