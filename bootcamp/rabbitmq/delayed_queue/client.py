# -*- coding: utf-8 -*-

import time, random, json, pika
import common

TTL = 60 * 1000
DELAY_QUEUE = 'delay_queue'

def _main():
    start_time = time.time()
    channel = common.get_channel()
    
    args = {
        'x-dead-letter-exchange': common.RETRY_EXCHANGE,
        # 'x-expires': TTL,
        'x-message-ttl': TTL
    }

    channel.queue_declare(
        queue=DELAY_QUEUE,
        arguments=args,
        # durable=True,
        auto_delete=True
    )

    # 发布消息
    for i in range(10):
        random_ttl = random.randint(1, 60) * 1000
        msg = json.dumps([i, random_ttl])
        channel.basic_publish(
            exchange='',
            routing_key=DELAY_QUEUE,
            body=msg,
            properties=pika.BasicProperties(
                delivery_mode=1,
                type='',
                expiration=str(random_ttl)
            )
        )
        print('Delivery: %s' % msg)
    print("client timeout: %0.6f" % (time.time() - start_time))


if __name__ == '__main__':
    _main()


