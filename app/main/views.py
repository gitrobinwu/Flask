#-*- coding:utf-8 -*- 
from flask import render_template, abort
from . import main
from ..models import User


@main.route('/')
def index():
    return render_template('index.html')

# 返回用户资料页面
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


