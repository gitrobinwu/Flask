#-*- coding:utf-8 -*- 
from flask import Flask
from flask_script import Manager

app = Flask(__name__)

# 把app传递给Manager对象，以初始化Flask Script 	
manager = Manager(app)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

# python hello.py runserver -h 0.0.0.0 -p 5006 
if __name__ == '__main__':
    manager.run()


