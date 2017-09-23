#-*- coding:utf-8 -*- 
from functools import wraps 
from flask import g,request,redirect,url_for

# 登录装饰器
def login_required(f):
	@wraps(f)
	def decorated_function(*args,**kwargs):
		if g.user is None:
			return redirect(url_for('login',next=reuqest.url))
		return f(*args,**kwargs)
	return decorated_function 

# 终端装饰器
from flask import Flask
from werkzeug.routing import Rule

app = Flask(__name__)
app.url_map.add(Rule('/',endpoint='index'))

@app.endpoint('index')
def my_index():
	return "Hello world"


