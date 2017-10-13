#-*- coding:utf-8 -*- 
import flask_whooshalchemyplus
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from jieba.analyse.analyzer import ChineseAnalyzer

import os 
from datetime import datetime 
basedir = os.path.abspath(os.path.dirname(__file__))

# set the location for the whoosh index
app = Flask(__name__)
app.config['WHOOSH_BASE'] = './base'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DETABASE_URI') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

# 跟踪修改		
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 请求尾部自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# sql回显
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class BlogPost(db.Model):
	__tablename__ = 'blogpost'
	__searchable__ = ['title', 'body']  # these fields will be indexed by whoosh
	__analyzer__ = ChineseAnalyzer() # 使用中文分词器

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	body = db.Column(db.Text)   # Unicode, or Text
	created = db.Column(db.DateTime, default=datetime.utcnow)


flask_whooshalchemyplus.whoosh_index(app,BlogPost)		

if __name__ == '__main__':
	db.drop_all()
	db.create_all()

	p1 = BlogPost(title=u"post1",body=u'天气好，开心')
	p2 = BlogPost(title=u'post2',body=u'my second post')
	p3 = BlogPost(title=u'post3',body=u'my third and last post')
	db.session.add_all([p1,p2,p3])
	db.session.commit()
	
	print '1111111'
	# 搜索
	print BlogPost.query.whoosh_search(query=u'post',fields=[u'body'])
