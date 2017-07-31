#-*- coding:utf-8 -*- 
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

# 将权限添加到程序上下文，以便在模板中调用
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
