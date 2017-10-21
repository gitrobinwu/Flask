#-*- coding:utf-8 -*- 
from flask import redirect,url_for,request,flash
from flask_admin import BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from ..models import Role,User,Post,Category,Tag
from .. import db
from flask_login import current_user 
import os

static_basedir = r'/home/robin/flask/Flask/project/app/static'


# 首页路由 /admin		
class MyAdminIndexView(AdminIndexView):
	# 检测是否为管理员
	def is_accessible(self):
		return current_user.is_administrator()
	
	# 跳转到登录页面	
	def inaccessible_callback(self, name, **kwargs):
		flash(u"非管理员操作")	
		return redirect(url_for('auth.login',next=request.url))
# 模型请求
class CustomViewBase(ModelView):
	def is_accessible(self):
		return current_user.is_administrator()

	def inaccessible_callback(self, name, **kwargs):
		flash(u"非管理员操作")	
		return redirect(url_for('auth.login',next=request.url))

# 定制化模型视图
class CustomRoleView(CustomViewBase):
	can_create = False
	# 该模型视图中需要显示的字段
	column_list=( "id","name","users")
	column_labels = {
		'id': u'序号',
		'name': u'名称',
		'users': u"用户列表"
	}

	column_formatters = dict(
		users=lambda v, c, m, p: (m.get_users),
	)

	# 添加要搜索的字段 
	column_searchable_list = ('name',) 

class CustomUserView(CustomViewBase):
	can_create = False
	column_list = ('id','username','email','password_hash','role','confirmed')
	column_labels = {
		'id': u'序号',
		'username': u'用户名',
		'email': u'邮箱',
		'password_hash': u'密码',
		'role': u'角色',
		'confirmed': u'是否确认',

	}
	# 只显示密码后六位
	column_formatters = dict(
		password_hash = lambda v, c, m, p: '**'+m.password_hash[-6:],
	)
	column_searchable_list = ('username','email') 

class CustomPostView(CustomViewBase):
	can_create = False
	column_list = ('id','title','create_time','author')
	column_labels = {
		'id': u'序号',
		'title': u'标题',
		'create_time': u'发表时间',
		'author': u'作者'
	}
	column_searchable_list = ('title',)

class CustomCategoryView(CustomViewBase):
	can_create = False
	column_list = ('id','name','author')
	column_labels = {
		'id': u'序号',
		'name': u'分类名称',
		'author': u'归属用户'
	}
	column_searchable_list = ('name',)
	
class CustomTagView(CustomViewBase):
	can_create = False
	column_list = ('id','name','author')
	column_labels = {
		'id': u'序号',
		'name': u'标签名称',
		'author': u'归属用户'
	}
	column_searchable_list = ('name',)	

# 添加视图
def admin_site(endpoint):
	# 增加模型视图
	endpoint.add_view(CustomRoleView(Role,db.session,name=u"角色"))
	endpoint.add_view(CustomUserView(User,db.session,name=u"用户"))
	endpoint.add_view(CustomPostView(Post,db.session,name=u"文章"))
	endpoint.add_view(CustomCategoryView(Category,db.session,name=u"分类"))
	endpoint.add_view(CustomTagView(Tag,db.session,name=u"标签"))

	# 增加文件管理
	endpoint.add_view(FileAdmin(static_basedir,name=u"管理文件"))	

if __name__ == '__main__':
	print static_basedir


