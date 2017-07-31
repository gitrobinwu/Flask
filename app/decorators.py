#-*- coding:utf-8 -*- 
from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

# 权限检查
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# admin 权限检查
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
