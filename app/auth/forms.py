#-*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField 
from wtforms.validators import DataRequired,Length,Email,EqualTo,Regexp
from wtforms import ValidationError
from ..models import User 

# 登录表
class LoginForm(FlaskForm):
	email = StringField(label=u'邮箱',validators=[DataRequired(),Length(1,64),Email()])
	password = PasswordField(label=u'密码',validators=[DataRequired()])
	remember_me = BooleanField(label=u'记住我')
	submit = SubmitField(label=u'登录')
	
# 注册表
class RegisterForm(FlaskForm):
	email = StringField(label=u'邮箱',validators=[DataRequired(),Length(1,64),Email()])
	username = StringField(label=u'用户名', validators=[DataRequired(), Length(1, 64), 
			Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,u'用户名只能包含字母、数字、下划线和点号')])
	password = PasswordField(label=u'密码',validators=[DataRequired(),
			EqualTo('password2',message=u'密码必须相同')])
	password2 = PasswordField(label=u'确认密码',validators=[DataRequired()])
	submit = SubmitField(label=u'马上注册')
	
	def validate_email(self,field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError(u'该邮箱已经被注册.')

	def validate_username(self,field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已经存在.')

# 更改密码
class ChangePasswordForm(FlaskForm):
	old_password = PasswordField(label=u'旧密码',validators=[DataRequired()])
	password = PasswordField(label=u'新密码',validators=[DataRequired(),
			EqualTo('password2',message=u'密码必须相同')])
	password2 = PasswordField(label=u'确认密码',validators=[DataRequired()])
	submit = SubmitField(label=u'更新')
			
