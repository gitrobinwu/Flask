#-*- coding:utf-8 -*- 
from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..models import User, AnonymousUser
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
	# 允许匿名用户
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
	# 允许使用令牌认证	
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
	
	# 普通认证	
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


# api 任何路由请求之前需要认证	
@api.before_request
@auth.login_required
def before_request():
	# 普通未认证用户则拒绝
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden('Unconfirmed account')


# 以普通认证方式登录请求新令牌		
@api.route('/token')
def get_token():
	# 匿名用户或者令牌认证登录则拒绝
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})
