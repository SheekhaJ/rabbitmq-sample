import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

exchangeName = 'logs'

channel.exchange_declare(exchange=exchangeName, exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queueName = result.method.queue

channel.queue_bind(exchange=exchangeName, queue=queueName)

print('[*] Waiting for logs. To exit press Ctrl+C')

def callback(ch, method, properties, body):
    print(f'[x] {body}')

channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=True)

channel.start_consuming()