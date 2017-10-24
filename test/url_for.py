
#-*- coding:utf-8 -*-
from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')	
@app.route('/<path:name>')
def index(name):
	pass

@app.route('/login')
def login():
	pass

with app.test_request_context():
	print(url_for('index'))
	print(url_for('index',name='robin',page=1,test='test'))
	print(url_for('login'))
