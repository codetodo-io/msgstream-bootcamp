# -*- coding: utf-8 -*-

import sys, time, pika, random
import common


def _main():
    number = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    channel = common.get_channel()
    queue_name = common.QUEUE_NAME
    start_time = time.time()
    # 发布消息
    for i in range(number):
        priority = random.randint(1, 10)
        message = 'message#{index}-with-priority{priority}'.format(
            index = i + 1, priority = priority
        )
        channel.basic_publish(
            properties=pika.BasicProperties(priority=priority),
            exchange='',
            routing_key=queue_name,
            body=message
        )
        # print('Publised: ', message)
    total_time = time.time() - start_time
    print("client %d, timeout: (%0.6f, %0.6f)" % (number, total_time, total_time / float(number)))


if __name__ == '__main__':
    _main()