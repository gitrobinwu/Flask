#-*- coding:utf-8 -*- 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#import flask_whooshalchemyplus
import flask_whooshalchemy as whooshalchemy
from jieba.analyse.analyzer import ChineseAnalyzer

import os 
from datetime import datetime 
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DETABASE_URI') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 搜索索引数据库 
# set the location for the whoosh index
app.config['WHOOSH_BASE'] = os.path.join(basedir, 'search.db')

db = SQLAlchemy(app)

class Post(db.Model):
	# 包含数据库能被搜索且建立索引的字段
	__tablename__ = 'posts'
	__searchable__ = ['title1','body1'] # these fields will be indexed by whoosh
	__analyzer__ = ChineseAnalyzer() # 使用中文分词器

	id = db.Column(db.Integer,primary_key=True)
	title1 = db.Column(db.String(64))
	body1 = db.Column(db.Text)
	timestamp1 = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 时间戳

	def __init__(self,title1,body1):
		self.title1 = title1 
		self.body1 = body1 

	def __repr__(self):
		return '<Post %r>' % self.title1 

class BlogPost(db.Model):
	# 包含数据库能被搜索且建立索引的字段
	__tablename__ = 'blogposts'
	__searchable__ = ['title','body'] # these fields will be indexed by whoosh
	__analyzer__ = ChineseAnalyzer() # 使用中文分词器

	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(64))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 时间戳

	def __init__(self,title,body):
		self.title = title 
		self.body = body 

	def __repr__(self):
		return '<Post %r>' % self.title 

#  初始化全文搜索索引 		
#flask_whooshalchemyplus.whoosh_index(app,BlogPost)		
whooshalchemy.whoosh_index(app,Post)	
whooshalchemy.whoosh_index(app,BlogPost)	

if __name__ == '__main__':
	db.drop_all()
	db.create_all()

	p1 = BlogPost(title="post1",body='my first post')
	p2 = BlogPost(title='post2',body='my second post')
	p3 = BlogPost(title='post3 second',body='my third and last post')
	p4 = BlogPost(title='post 4',body='this is a test')

	p5 = BlogPost(title=u'测试',body=u'这是一个标题')
	p6 = BlogPost(title=u'内容',body=u'号百这是一个测试')
	p7 = BlogPost(title=u'百度',body=u'号百八度')
	p8 = BlogPost(title=u'全文搜索',body=u'天气好，开心')
	db.session.add_all([p1,p2,p3,p4,p5,p6,p7,p8])
	db.session.commit()

	# 搜索
	print BlogPost.query.whoosh_search('post').all() # 同时搜索title,body OK
	print BlogPost.query.whoosh_search('second').all() # title 或者 body 至少有一个包含
	print BlogPost.query.whoosh_search('second last').all()# 英文搜索多词词组必须用空格间隔，否则视为单一词组
	print '-'*60
	#任意特殊字符和单字母字符都可以切割，默认AND
	for i in BlogPost.query.whoosh_search(u'测试 号百').all():print i.title # title 或者 body分词后词组中必须包含所有词组
	print "#####################"
	for i in BlogPost.query.whoosh_search(u'测试 号百',or_=False).all():print i.title # OR 知识包含一个
	for i in BlogPost.query.whoosh_search(u'测试 OR 号百').all():print i.title # OR 知识包含一个
	print '-'*60
	print BlogPost.query.whoosh_search(u'天气好').all()[0].title
	print BlogPost.query.whoosh_search(u'搜索').all()[0].title

	print '*'*30
	p11 = Post(title1="post1",body1='my first post')
	p22 = Post(title1='post2',body1='my second post')
	db.session.add_all([p11,p22])
	db.session.commit()
	
	print Post.query.whoosh_search('post').all()
	


