import pika
import time
from datetime import datetime

sleepTime = 10
print(' [*] Sleeping for ', sleepTime, ' seconds.')
time.sleep(30)
exchangeName = 'jobs'

print(' [*] Connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

queueName = ''

channel.exchange_declare(exchange=exchangeName, exchange_type='fanout')

result = channel.queue_declare(queue=queueName, durable=True)
queueName = result.method.queue

channel.queue_bind(exchange=exchangeName, queue=queueName)

print(' [*] Waiting for messages.')


def callback(ch, method, properties, body):
    cmd = body.decode()
    print(f' [x] Received command - {body} at {datetime.now()}')
    print(" [x] Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queueName, on_message_callback=callback)
channel.start_consuming()