#-*- coding:utf-8 -*- 
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	# 应用密匙
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	# 将其设置为True时，每次请求结束后自动提交数据库的变动
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	# 邮箱服务器配置
	MAIL_SERVER = 'mx.besttone.com.cn'
	MAIL_PORT = 25
	MAIL_USE_TLS = False  
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "wuyongwei"
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "123456"
	# FLASKY_MAIL_SUBJECT_PREFIX = '[Robin]'
	FLASKY_MAIL_SENDER = 'wuyongwei<wuyongwei@besttone.com.cn>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or '694380339@qq.com' 
	
	# 默认每页显示的记录数量
	FLASKY_POSTS_PER_PAGE = 10

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	#SQLALCHEMY_DATABASE_URI = "mysql://root:abc123@localhost/blog?charset=utf8"
	SQLALCHEMY_DATABASE_URI = "mysql://root:abc123@localhost/blog"

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}


