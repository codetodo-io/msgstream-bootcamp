# -*- coding: utf-8 -*-

import os, pika, uuid, time

def fib(n):
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


class RPCServer(object):

    def __init__(self):
        # 连接RabbitMQ并获取频道
        urls = os.environ.get('RABBITMQ_ADDRESS')
        all_endpoints = [pika.URLParameters(url) for url in urls.split(',')]
        self.connection = pika.BlockingConnection(all_endpoints)
        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue='rpc_queue',
            arguments={'x-max-priority': 10},
            auto_delete=True
        )
        self.channel.basic_qos(prefetch_count=1)

        self.channel.basic_consume(
            queue='rpc_queue',
            on_message_callback=self.on_request,
        )

    def on_request(self, ch, method, props, body):
        n = int(body)
        print(n)
        response = fib(n)

        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(
                correlation_id=props.correlation_id
            ),
            body=str(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.start_consuming()
    

if __name__ == '__main__':
    rpc = RPCServer()
    rpc.run()