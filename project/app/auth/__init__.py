#-*- coding:utf-8 -*- 
from flask import Blueprint 

# 认证蓝本
# 未注册时，蓝本处于睡眠状态
auth = Blueprint('auth',__name__)

from . import views



