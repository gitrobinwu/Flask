#-*- coding:utf-8 -*- 
from flask_msearch import Search
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os 
from datetime import datetime 
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DETABASE_URI') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MSEARCH_INDEX_NAME '] = 'whoosh_index'
app.config['MSEARCH_BACKEND '] = 'whoosh'
app.config['MSEARCH_ENABLE'] = True 

db = SQLAlchemy(app)
search = Search(db=db)
search.init_app(app)

class BlogPost(db.Model):
	__tablename__ = 'blogpost'
	__searchable__ = ['title', 'body']  # these fields will be indexed by whoosh

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	body = db.Column(db.Text)   # Unicode, or Text
	created = db.Column(db.DateTime, default=datetime.utcnow)

db.drop_all()
db.create_all()

search.create_index(update=True) 

if __name__ == '__main__':

	p1 = BlogPost(title="post 1",body='my first post')
	p2 = BlogPost(title='post 2',body='my second post')
	p3 = BlogPost(title='post 3',body='my third and last post')
	db.session.add_all([p1,p2,p3])
	db.session.commit()

	# 搜索
	print search.whoosh_search(BlogPost,query='post',fields=['body'],limit=20).all()
	"""print BlogPost.query.filter(BlogPost.title.startswith('post'))
	print BlogPost.query.msearch('post',fields=['title'],limit=20)
	BlogPost.query.msearch('second',fields=['title'])"""
	
