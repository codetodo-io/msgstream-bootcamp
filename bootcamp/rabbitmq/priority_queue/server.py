# -*- coding: utf-8 -*-

import time, pika
import common

def callback(ch, method, properties, body):
    # print('Received: %s' % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def _main():
    channel = common.get_channel()
    queue_name = common.QUEUE_NAME

    start_time = time.time()
    try:
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )
        # print('Waiting for message. To exit press CTRL+C.')
        channel.start_consuming()
    except pika.exceptions.ChannelClosedByBroker:
        pass
    print("server timeout: %0.6f" % (time.time() - start_time))
    

if __name__ == '__main__':
    _main()