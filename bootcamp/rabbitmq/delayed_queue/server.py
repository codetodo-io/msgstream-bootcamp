# -*- coding: utf-8 -*-

import time
import common

def _message_handle_successfully(channel, method):
    channel.basic_ack(delivery_tag=method.delivery_tag)

def _message_handle_failed(channel, method):
    channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)

def callback(ch, method, properties, body):
    msg = body.decode()
    print('Received: %s' % body)
    _message_handle_successfully(ch, method)


def _main():
    start_time = time.time()

    channel = common.get_channel()
    channel.queue_declare(
        queue=common.RETRY_QUEUE,
        # durable=True,
        auto_delete=True
    )
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=common.RETRY_QUEUE,
        on_message_callback=callback
    )
    channel.start_consuming()
    print("server timeout: %0.6f" % (time.time() - start_time))


if __name__ == '__main__':
    _main()
