import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

exchangeName='logs'

channel.exchange_declare(exchange=exchangeName,exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or 'info: Hello World!'
channel.basic_publish(exchange=exchangeName, routing_key='', body=message)
print(f'[x] Sent {message}')
connection.close()