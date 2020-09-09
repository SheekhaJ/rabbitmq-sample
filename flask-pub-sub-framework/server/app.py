import os
from flask import Flask, request, flash, redirect, url_for
import pika
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
uploadFolder = './../model-user-uploads/'

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = uploadFolder

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return '''
        <!doctype html>
        <title>Upload MNIST image file</title>
        <form method=post enctype=multipart/form-data>
        <h1>Job 1 - Upload MNIST image file</h1>
        <input type=file name=mnistfile>

        <h1>Job 2 - Upload CIFAR image file</h1>
        <input type=file name=cifarfile>
        </br>

        <p><input type=submit value='Submit Jobs'></p>

        </form>
        '''
    elif request.method == 'POST':
        print(request.files)
        # check if the post request has the file part
        if 'mnistfile' not in request.files :
        # or 'cifarfile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        mnistfile = request.files['mnistfile']
        # cifarfile = request.files['cifarfile']
        # if user does not select file, browser also
        # submit an empty part without filename
        if mnistfile.filename == '':
            flash('No selected file')
            return redirect(request.url)
            # return f'1) filename - {file.filename}'
        if mnistfile and allowed_file(mnistfile.filename):
            filename = secure_filename(mnistfile.filename)
            mnistfile.save(os.path.join(app.config['UPLOAD_FOLDER']+'/mnist/', filename))
            # return redirect(url_for('uploaded_file', filename=filename))
            # return f'2) filename - {file.filename}'
            return redirect(url_for('mnistModels',mnistfilename=filename),code=302)

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/models/mnist/<mnistfilename>',methods=['GET','POST'])
def mnistModels(mnistfilename):
    return f'Invoked mnist model service type of request - {request.method} and filename is {mnistfilename}!'
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')