#-*- coding:utf-8 -*- 
from flask import render_template,redirect,request,url_for,flash 
from flask_login import login_user,logout_user,login_required,current_user 
from . import auth 
from .. import db 
from ..models import User 
from ..email import send_email 
from .forms import LoginForm,RegisterForm,ChangePasswordForm

# 账户登录
@auth.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm() 
	# from.validate_on_submit()相当于form.is_submitted() and form.validate() 
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first() 
		if user is not None and user.verify_password(form.password.data): #密码验证成功
			# 在用户会话中把用户标记为已登录
			login_user(user,form.remember_me.data)
			# 防止再跳转回来，提示不合适的信息
			if request.endpoint[:5] != 'auth.':
				flash(u'欢迎回来%s' % user.username)
			# 用户访问未授权的URL时会显示登录表单，Flask-Login会把原地址保存在查询字符串next参数
			# 这个参数可从request.args字典中读取
			return redirect(request.args.get('next') or url_for('main.index'))
		flash(u'账号或者密码错误')
	return render_template('auth/login.html',form=form)

# 注销账户
@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(u'您已注销账户.')
	return redirect(url_for('main.index'))

# 注册账户
@auth.route('/register',methods=['GET','POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		# 添加新用户到数据库
		user = User(email=form.email.data,
				username=form.username.data,
				password=form.password.data)
		db.session.add(user)
		db.session.commit()
		# 生成用户令牌
		token = user.generate_confirmation_token() 
		# to subject template **kwargs 
		send_email(user.email,u'请确认您的账号','auth/email/confirm',user=user,token=token) # 发邮件
		flash(u'有一份邮件已经发往您的邮箱')
		return	redirect(url_for('auth.login'))
	return render_template('auth/register.html',form=form)

# 确认账户可以联系上，才有权限进行其他操作
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	# 防止重复确认
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(u'感谢您的确认')
	else:
		flash(u'链接已经失效或者过期')
	return redirect(url_for('main.index'))	

# 对程序全局请求的钩子，必须使用before_app_request 修饰器	 
@auth.before_app_request
def before_request():
	if current_user.is_authenticated:
		# 更新已登录用户的访问时间 
		current_user.ping()
		# 如果用户已登录，用户账户还未确认，请求的端点不在auth认证蓝本中
		if  not current_user.confirmed \
				and request.endpoint \
				and request.endpoint[:5] != 'auth.' \
				and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))

# 如果当前是匿名帐号活着已经确认，直接返回首页，否则显示未确认
@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	return render_template('auth/unconfirmed.html')

# 再次确认账户
@auth.route('/resend_email')
@login_required
def resend_email():
	token = current_user.generate_confirmation_token()
	send_email(current_user.email,u'请确认您的账号','auth/email/confirm',user=current_user,token=token) # 发邮件
	flash(u'有一份新邮件已经发往您的邮箱')
	return redirect(url_for('main.index')) 

# 更改账户密码
@auth.route('/change-password',methods=['GET','POST'])
@login_required
def change_password():
	form = ChangePasswordForm() 
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			flash(u'您的密码已经更新')
			return redirect(url_for('main.index'))
		else:
			flash(u'旧密码输入有错误')
	return render_template("auth/change_password.html",form=form)


