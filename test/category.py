#-*- coding:utf-8 -*- 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DETABASE_URI') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
db = SQLAlchemy(app)

# 文章		
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 时间戳
	
	# 建立分类到文章的一对多关系
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	category = db.relationship('Category',backref=db.backref('posts', lazy='dynamic'))

	def __repr__(self):
		return '<Post.title %r>' %self.title

# 分类	
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tag = db.Column(db.String(64))
	count =db.Column(db.Integer, default=1)

	def __repr__(self):
		return '<Category %r>' %self.tag

if __name__ == '__main__':
	db.drop_all()
	db.create_all()

	'''cat = Category('python')
	post = Post('python','hello python')
	db.session.add(cat)
	db.session.add(post)
	db.session.commit() #提交'''

	py = Category(tag='Python')
	py1 = Category(tag='Python1')
	p1 = Post(title='Hello Python!', body='Python is pretty cool', category=py)
	p2 = Post(title='Hello again!', body='Python is pretty cool', category=py)
	p2 = Post(title='Hello again1!', body='Python is pretty 21cool', category=py)
	db.session.add_all([py,py1,p1,p2])
	db.session.commit()
	
	print py.posts.all(),len(py.posts.all())


