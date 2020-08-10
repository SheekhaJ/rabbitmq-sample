import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
sentBody = 'Hello World 5!'
channel.basic_publish(exchange='',routing_key='hello',body=sentBody)

print(f"[x] Sent {sentBody}!")

connection.close()