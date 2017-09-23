#-*- coding:utf-8 -*- 
#使用WTForms进行表单验证
# 要使用WTForms需要先定义表单为类，为表单定义一个独立的模块

# 注册页面表单
from wtforms import Form,BooleanField,TextField,PasswordField,validators 
class RegistrationForm(Form):
	username = TextField('Username',[validators.Length(min=4,max=25)])
	email = TextField('Email Address',[validators.Length(min=6,maxx=35)])
	password = PasswordField('New Password',[
			validators.Required(),
			validators.EqualTo('confirm',message="Passwords must match")
		])
	confirm = PasswordField('Repeat Password')
	accept_tos = BooleanField('I accept the TOS',[validators.Required()])



