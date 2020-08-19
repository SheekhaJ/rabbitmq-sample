from flask import Flask
from flask import request
import pika

app = Flask(__name__)
exchangeName = 'cmds'

@app.route('/cmds/<cmd>', methods=['GET'])
def addCmd(cmd):
    # if request.method == 'GET':
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangeName, exchange_type='fanout')
    print(f'printing received command - {cmd}')
    channel.basic_publish(exchange=exchangeName, routing_key='', body=cmd)
    connection.close()
    return '[x] Sent cmd {}'.format(cmd)

