#-*- coding:utf-8 -*- 
from flask import Blueprint

# 通过实例化一个Blueprint类对象创建蓝本
# 蓝本名和蓝本所在包或模块
main = Blueprint('main', __name__)

from . import views, errors
