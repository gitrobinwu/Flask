#-*- coding:utf-8 -*- 
from flask import Flask
from flask import render_template 
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime 
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DETABASE_URI') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
db = SQLAlchemy(app)

# 分类	
class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tag = db.Column(db.String(64))
	count =db.Column(db.Integer, default=0)
	# lazy 说明如何加载记录
	# subquery 会在加载 Post 对象后，将与 Post 相关联的对象全部加载，这样就可以减少 Query 的动作 
	# dynamic 只有被使用时，对象才会被加载，并且返回式会进行过滤
	posts = db.relationship('Post',backref=db.backref('category',lazy='subquery'),lazy='dynamic')

	def __init__(self,tag):
		self.tag = tag

	def __repr__(self):
		return '<Category %r>' %self.tag

# 文章
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(64))
	body = db.Column(db.Text)
	# 建立关系
	category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
	# 添加关系的面向对象视角
	# 第一个参数  关联模型
	# 第二个参数 建立双向关系，反向代理
	# 第三个参数 说明如何加载记录
	#category = db.relationship('Category',backref=db.backref('posts',lazy='dynamic'))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 时间戳

	def __init__(self,title,body,category):
		self.title = title
		self.body = body
		self.category = category
		self.category.count +=1
		
	def __repr__(self):
		return '<Post.title %r>' %self.title
		
# 添加视图
@app.route('/')
def index():
	# 获取所有的分类
	categorys = Category.query.order_by(Category.count)[::-1]
	# 循环显示
	return render_template('index.html', categorys=categorys)

#返回改标签下的所有文章	
@app.route('/category/<tag>')
def category(tag):
	category = Category.query.filter_by(tag=tag).first_or_404()
	posts = category.posts.all()
	return render_template('post.html',posts=posts)
		
# 模型 --> 视图 --> 前端 
if __name__ == '__main__':
	db.drop_all()
	db.create_all() 
	
	# 分类
	py1 = Category('Python')
	py2 = Category('HTML')
	py3 = Category('C++')
	db.session.add_all([py1,py2,py3])
	db.session.commit() 
	#文章
	p1 = Post('Hello Python-1!', 'Python is pretty cool--1', py1)
	p2 = Post('Hello Python-2!', 'Python is pretty cool--2', py1)
	pa = Post('Hello Python-a!', 'Python is pretty cool--a', py1)
	p3 = Post('Hello HTML-1!', 'HTML is pretty cool--1', py2)
	p4 = Post('Hello HTML-2!', 'HTML is pretty cool--2', py2)
	p5 = Post('Hello C++-1!', 'C++ is pretty cool--1', py3)
	p6 = Post('Hello C++-2!', 'C++ is pretty cool--2', py3)
	db.session.add_all([p1,p2,pa,p3,p4,p5,p6])
	db.session.commit()
		

	# 查看分类下的所有文章
	print py1.posts.all() 
	print py1.count 
	print py2.posts.all() 
	print py3.count 
	print py2.posts.all() 
	print py3.count 

	# 查看文章的所属分类
	print p1.category
	app.run(host='0.0.0.0',port=5012)












