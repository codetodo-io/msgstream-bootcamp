# -*- coding: utf-8 -*-

import os, pika

# 设置队列名
QUEUE_NAME = 'priority-queue'
# 设置最高等级，超出10按10进行排序
MAX_PRIORITY = 10

def get_channel():
    # 连接RabbitMQ并获取频道
    urls = os.environ.get('RABBITMQ_ADDRESS')
    all_endpoints = [pika.URLParameters(url) for url in urls.split(',')]
    connection = pika.BlockingConnection(all_endpoints)
    channel = connection.channel()
    # 创建队列并设置最大优先等级
    channel.queue_declare(
        queue=QUEUE_NAME,
        arguments={'x-max-priority': MAX_PRIORITY},
        auto_delete=True
    )
    channel.basic_qos(prefetch_count=1)
    return channel
