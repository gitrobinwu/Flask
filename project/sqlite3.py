#-*- coding:utf-8 -*- 
import sqlite3
from flask import g

DATABASE = '/path/to/database.db'

def connect_db():
	return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
	g.db = connect_db()

# teardown request 在请求结束时总会运行，即使before-request处理器运行失败或者从未运行过	
@app.teardown_request
def teardowm_request(exception):
	if hasattr(g,'db'):
		g.db.close() 

#2,按需连接
def get_connection():
	db = getattr(g,'_db',None)
	if db is None:
		db = g._db = connect_db()
	return db 

#3, 


