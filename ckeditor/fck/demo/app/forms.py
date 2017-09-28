#-*- coding:utf-8 -*-
from flask_wtf import FlaskForm 
from wtforms import TextAreaField,SubmitField,StringField 
from flaskckeditor import CKEditor 

# CK 表单
class CKEditorForm(FlaskForm,CKEditor):
	title = StringField()
	ckdemo = TextAreaField()
	submit = SubmitField() 

if __name__ == '__main__':
	for i,k in CKEditor.__dict__.items():
		if i.startswith(r'__'): continue 						
		print '\n',i,k


