#-*- coding:utf-8 -*- 
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# 基类Config包含通用配置，子类分别定义专用配置
# 为了让配置方式更灵活且更安全，某些配置可以从环境变量中导入
class Config:
	# 这是个敏感信息，可以在环境中设定，但系统也提供了一个默认值，以防环境中没有定义
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	# 将其设为True时，每次请求结束后自动提交数据库的变动
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'mx.besttone.com.cn'
    MAIL_PORT = 25
    MAIL_USE_TLS = False 
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_USERNAME = "wuyongwei"
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PASSWORD = "123456"
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'wuyongwei@besttone.com.cn'
    #FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_ADMIN = "wuyongwei@besttone.com.cn"
	
	# 执行对当前环境的配置初始化
    @staticmethod
    def init_app(app):
        pass

# SQLALCHEMY_DATABASE_URI 变量了不同的值，这样程序就可在不同的配置环境中运行
# 每个环境使用不同的数据库
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

# 注册不同的配置环境，并注册一个默认配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
