#-*- coding:utf-8 -*-
from . import app
from flask import render_template,redirect,url_for,request 
from .forms import CKEditorForm

@app.route('/',methods=['GET','POST'])
def index():
	form = CKEditorForm()
	if form.validate_on_submit():
		#print request.form['ckdemo']
		print form.ckdemo.data
		return redirect(url_for('.index'))
	return render_template('index.html',form=form)


# 上传	
@app.route('/ckupload/', methods=['GET','POST'])
def ckupload():
	form = CKEditorForm() 
	return form.upload(endpoint=app)
	
