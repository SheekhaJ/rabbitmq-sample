from flask import Flask, request, flash, redirect
import pika

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'

exchangeName = 'jobs'

@app.route('/add-job/<cmd>')
def add(cmd):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchangeName, exchange_type='fanout')
    # channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange=exchangeName,
        # routing_key='task_queue',
        routing_key='',
        body=cmd,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
        )
    connection.close()
    return " [x] Sent: %s" % cmd

@app.route('/models/mnist',methods=['GET','POST'])
def mnistModels():
    if request.method == 'POST':
        # return 'POST request received!'
        if 'file' not in request.files:
            flash('No file uploaded!')
            return redirect(request.url)
        else:
            file = request.files['file']
            return f'Received file {file}'
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload MNIST image file</title>
        <h1>Upload MNIST image file</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')