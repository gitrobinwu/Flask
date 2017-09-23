#-*- coding:utf-8 -*- 
from flask import Flask 
from database import db_session 

app = Flask(__name__)

# 在请求结束时自动移除数据库会话
@app.teardown_request()
def shutdown_session(exception=None):
	db_session.remove() 



