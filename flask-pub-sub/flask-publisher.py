from flask import Flask
from flask import request
import pika

app = Flask(__name__)
exchangeName = 'cmds'

@app.route('/cmds/<cmd>', methods=['GET'])
def addCmd(cmd):
    if request.method == 'GET':
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchangeName, exchange_type='fanout')
        channel.basic_publish(exchange=exchangeName, routing_key='', body=cmd)
        connection.close()
        return '[x] Sent cmd {}'.format(cmd)

@app.route('/')
def hello():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')