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
whooshalchemy.whoosh_index(app, BlogPost)	

if __name__ == '__main__':
	db.drop_all()
	db.create_all()

	p1 = BlogPost(title="post1",body='my first post')
	p2 = BlogPost(title='post2',body='my second post')
	p3 = BlogPost(title='post3',body='my third and last post')
	p4 = BlogPost(title='post 4',body='this is a test')

	p5 = BlogPost(title='chineese test1',body=u'天气好，开心')
	db.session.add_all([p1,p2,p3,p4,p5])
	db.session.commit()

	# 搜索
	print BlogPost.query.whoosh_search('post').all() # 同时搜索title,body 
	print BlogPost.query.whoosh_search('second').all()
	print BlogPost.query.whoosh_search('second OR last').all()
	print '-'*60
	print BlogPost.query.whoosh_search(u'开心').all()[0].title
	print BlogPost.query.whoosh_search(u'天气好').all()[0].title
	print BlogPost.query.whoosh_search(u'天气').all()[0].title
	
	
