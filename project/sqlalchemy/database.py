#-*- coding:utf-8 -*- 
# SQLAlchemy中的declarative扩展是最新的使用SQLAlchemy的方法。允许同时定义表和模型 
from sqlalchemy import create_engine 
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base 

engine = create_engine('sqlite:////tmp/test.db',convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
											autoflush = False,
											bind=engine))
Base = declarative_base()
Base.query = db_session.query_property() 

def init_db():
	# 在这里导入所有的可能与定义模型相关的模块，这样他们才会合适的在metadata中注册。
	# 否则，将不得不在第一次执行init_db()时先导入他们
	#import models
	Base.metadata.create_all(bind=engine)
# 为了定义模型，构造一个Base类的子类
	


