# -*- coding: utf-8 -*-

import os, pika

RETRY_EXCHANGE = 'retry_exchange'
RETRY_QUEUE = 'retry_queue'

def get_channel():
    # 连接RabbitMQ并获取频道
    urls = os.environ.get('RABBITMQ_ADDRESS')
    all_endpoints = [pika.URLParameters(url) for url in urls.split(',')]
    connection = pika.BlockingConnection(all_endpoints)
    channel = connection.channel()

    # 创建交换器、队列和绑定
    channel.exchange_declare(
        exchange=RETRY_EXCHANGE,
        exchange_type='fanout',
        # durable=True,
        auto_delete=True
    )
    channel.queue_declare(
        queue=RETRY_QUEUE,
        # durable=True,
        auto_delete=True
    )
    channel.queue_bind(RETRY_QUEUE, RETRY_EXCHANGE)

    return channel
