#-*- coding:utf-8 -*- 
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
		# 判断用户是否存在，密码是否正确
        if user is not None and user.verify_password(form.password.data):
			# 创建登录会话，标记用户已登录，以及否记住用户(写cookie)
            login_user(user, form.remember_me.data)
			# 用户访问未授权的URL 时会显示登录表单，Flask-Login会把原地址保存在查询字符串的next 参数中
			# 这个参数可从request.args 字典中读取
			# 如果查询字符串中没有next 参数，则重定向到首页 
            return redirect(request.args.get('next') or url_for('main.index'))
		# 如果用户不存在或者密码错误，生成一个Flash 消息，再次渲染表单，让用户重试登录	
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	# 删除并重设用户会话
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


