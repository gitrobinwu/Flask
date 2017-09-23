#-*- coding:utf-8 -*- 
from sqlalchemy import Column,Integer,String
from database import Base 
from database import init_db,db_session
# 数据表和模型 一起定义
class User(Base):
	__tablename__ = 'users'
	id = Column(Integer,primary_key=True)
	name = Column(String(50),unique=True)
	email = Column(String(120),unique=True)

	def __init__(self,name=None,email=None):
		self.name = name 
		self.email = email 

	def  __repr__(self):
		return '<User %r>' % (self.name)

if __name__ == '__main__':
	#  创建数据库
	init_db() 
	# 写用户数据到数据库 
	u = User('admin','admin@localhost')
	db_session.add(u)
	db_session.commit()

	#查询数据
	print User.query.all() 
	print User.query.filter(User.name == 'admin').first() 

