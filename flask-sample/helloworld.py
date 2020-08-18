from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index page!'

@app.route('/hello')
def hello():
    return 'Hello World page!'

@app.route('/user/generic/<username>')
def show_user_profile(username):
    return f'Username is {username}. len - {len(username)}'

@app.route('/user/string/<string:username>')
def show_user_profile_str(username):
    return f'Username is {username}. len - {len(username)} type is {type(username)}'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return f'Called POST method on /login route {request.method}'
    else:
        return f'Called GET method on /login route {request.method}'