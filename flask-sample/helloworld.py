from flask import Flask, url_for, render_template
from flask import request

app = Flask(__name__)

# Demonstration of usage of url_for() method to dynamically build URLs.
@app.route('/')
def index():
    print(f'URL for viewing generic username profile - {url_for("show_user_profile",username="Vanessa")}')
    print(f'URL for viewing string username profile - {url_for("show_user_profile_str",username="Jane")}')
    return 'Index page!'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html',name=name)
    # return 'Hello World page!'

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

# Accessing the URL with a trailing / or without will redirect to the loginwithslash page
@app.route('/loginwithslash/',methods=['GET'])
def loginwithslash():
    return f'Called GET method on /loginwithslash/ route {request.method}'

# Accessing the URL with a trailing / here will access the /loginwithslash/1 page 
# but without a trailing / will give 404 because the route has been mentioned with a trailing /
@app.route('/loginwithslash/1/',methods=['GET'])
def loginwithslash1():
    return f'Called GET method on /loginwithslash/1/ route {request.method}'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001',debug=True)