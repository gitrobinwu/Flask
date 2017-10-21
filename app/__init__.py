#-*- coding:utf-8 -*- 
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from config import config
import flask_whooshalchemy as whooshalchemy
from flask_admin import Admin
from flask_babelex import Babel

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
# None,basic,strong 提供不同的安全等级防止用户会话篡改 
login_manager.session_protection = 'strong'
# 设置登录页面的端点
login_manager.login_view = 'auth.login'

from .models import Post
import admin

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	# 初始化扩展对象 
	bootstrap.init_app(app)
	mail.init_app(app)
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	# 初始化全文搜索索引
	whooshalchemy.whoosh_index(app,Post)

	# 初始化admin站点
	flask_admin = Admin(
			app,
			name="Admin",
			template_mode='bootstrap3',
			index_view=admin.MyAdminIndexView(
				name=u"导航栏",
				url="/admin",
				template='admin/welcome.html',
				),
			)
	flask_babel = Babel(app)
	admin.admin_site(flask_admin)

	# 注册蓝本 
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	
	# 注册认证蓝本
	from .auth import auth as auth_blueprint 
	app.register_blueprint(auth_blueprint,url_prefix='/auth')

	return app


