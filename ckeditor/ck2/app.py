#-*- coding:utf-8 -*- 
import os 
import datetime 
import random 
from flask import Flask,request,render_template,url_for,make_response,redirect
from flaskckeditor import CKEditor

app = Flask(__name__)


# 首页路由	
@app.route('/',methods=['GET','POST'])
def index():
	if request.method == "POST":
		print '-'*60
		print request.form['ckeditor'] 
		print '-'*60
		redirect(url_for('index'))
	return render_template('index.html')

# 上传	
@app.route('/ckupload/', methods=['GET','POST'])
def ckupload():
	form = CKEditor()
	return form.upload(endpoint=app)

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5010)
	

