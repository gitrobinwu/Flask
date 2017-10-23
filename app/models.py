#-*- coding:utf-8 -*- 
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin 
from . import db,login_manager 
from lxml import html
import re
from jieba.analyse.analyzer import ChineseAnalyzer

# 按字节位定义权限常量,表示某操作权限
class Permission:
	FOLLOW = 0x01 # 关注用户
	COMMENT = 0x02 # 在他人的文章中发表评论
	WRITE_ARTICLES = 0x04 #写文章
	MODERATE_COMMENTS = 0x08 #管理他人发表的评论
	ADMINISTER = 0xff # 管理者权限

# 使用权限组织角色，以后添加新角色时只需使用不同的权限组合即可。	
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	# 只有一个角色的字段要设为True,其他都设为Fasle 
	default = db.Column(db.Boolean,default=False,index=True)
	# 不同角色权限不同
	permissions = db.Column(db.Integer)
	# Role对象引用users,Users对象引用role 
	users = db.relationship('User', backref='role', lazy='dynamic')

	@property
	def get_users(self):
		return self.users.all()

	# 要想添加新角色，或者修改角色的权限，修改roles 数组，再运行函数即可。
	# 注意，匿名角色不需要在数据库中表示出来，这个角色的作用就是为了表示不在数据库中的用户。
	@staticmethod 
	def insert_roles():
		roles = {
			'User': (Permission.FOLLOW |
					 Permission.COMMENT |
			         Permission.WRITE_ARTICLES, True),   # 只有普通用户的default为True
			'Moderare': (Permission.FOLLOW | 
					     Permission.COMMENT |
						 Permission.WRITE_ARTICLES | 
						 Permission.MODERATE_COMMENTS, False),
			'Administrator': (0xff, False)
		}
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit() 
			
	def __repr__(self):
		return '<Role %r>' % self.name


class User(UserMixin,db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64),unique=True,index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	# 使用werkzeug实现散列密码
	password_hash = db.Column(db.String(128))
	# 一个用户有一个角色，角色可属于多个用户
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	# 确认账户
	confirmed = db.Column(db.Boolean,default=False)

	# 新增用户头像
	real_avatar = db.Column(db.String(128),default=None)

	name = db.Column(db.String(64)) # 真实姓名
	location = db.Column(db.String(64)) # 所在地
	# db.String 和db.Text 的区别在于后者不需要指定最大长度 
	about_me = db.Column(db.Text()) # 自我介绍
	member_since = db.Column(db.DateTime(), default=datetime.utcnow) # 注册时间
	# 用户每次访问网站后，这个值都会被刷新 
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow) # 上次访问时间

	### 用户发表的博客文章
	posts = db.relationship('Post',backref='author',lazy='dynamic')

	### 该用户下建立的分类
	categorys = db.relationship('Category',backref='author',lazy='dynamic')

	### 该用户下建立的标签
	tags = db.relationship('Tag',backref='author',lazy='dynamic')

	# 该用户发表的评论
	comments = db.relationship('Comment',backref='author',lazy='dynamic')

	# 返回用户下分类名称集合
	def get_categorys_text(self):
		rst = list()
		for category in self.categorys:
			if category.name not in rst:
				rst.append(category.name)
		return rst

	# 返回用户下标签名称集合
	def get_tags_text(self):
		rst = list()
		for tag in self.tags:
			if tag.name not in rst:
				rst.append(tag.name)
		return rst

	# 生成一批虚拟用户数据
	@staticmethod 
	def generate_fake(count=100):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py

		seed()
		for i in range(count):
			u = User(email=forgery_py.internet.email_address(),
					username=forgery_py.internet.user_name(True),
					password=forgery_py.lorem_ipsum.word(),
					confirmed=True,
					name=forgery_py.name.full_name(),
					location=forgery_py.address.city(),
					about_me=forgery_py.lorem_ipsum.sentence(),
					member_since=forgery_py.date.date(True))
			db.session.add(u)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback() 
	
	# 删除所有的用户数据
	@staticmethod
	def delete_alluser():
		users = User.query.all()
		for user in users:
			# 先要删除用户对应的博客文章
			User.delete_user_posts(user.email)
			db.session.delete(user)
			db.session.commit() 

	# 添加有效的用户数据
	@staticmethod 		
	def add_user(email,username,password,confirmed=True):
		u = User(email=email,username=username,confirmed=True,password=password)
		db.session.add(u)
		db.session.commit() 
				
	# 删除指定用户发表的所有博客文章
	@staticmethod
	def delete_user_posts(email):
		user = User.query.filter_by(email=email).first()
		if user:
			for post in user.posts:
				db.session.delete(post)
				db.session.commit() 

	# 删除指定用户发表指定博客文章
	@staticmethod
	def delete_user_onepost(email,title):
		user = User.query.filter_by(email=email).first()
		if user:
			posts = Post.query.filter_by(title=title).all()
			if posts:
				for post in posts:
					db.session.delete(post)
					db.session.commit() 

	# 用户在注册账户时，会被赋予适当的角色
	def __init__(self,**kwargs):
		super(User,self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['FLASKY_ADMIN']: # 邮箱与管理者邮箱相同
				# 管理员角色
				self.role = Role.query.filter_by(permissions=0xff).first()
			if self.role is None:
				# 默认用户
				self.role = Role.query.filter_by(default=True).first() 

	# 访问password属性则抛出异常
	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	# 设置hash密码
	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	# 检测密码
	def verify_password(self,password):
		return check_password_hash(self.password_hash,password)

	# 生成用户令牌
	def generate_confirmation_token(self,expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'],expiration)
		return s.dumps({'confirm': self.id})

	# 检测用户令牌
	def confirm(self,token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		# 检测令牌中的用户标识是否是当前用户	
		if data.get('confirm') != self.id:
			return Fasle 	
		self.confirmed = True 
		db.session.add(self)
		return True 
	
	# 检查用户权限	
	def can(self,permissions):
		return self.role is not None and \
			(self.role.permissions & permissions) == permissions
	
	# 检查是否为管理者	
	def is_administrator(self):
		return self.can(Permission.ADMINISTER)
	
	# 刷新用户的最后访问时间 
	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

	def __repr__(self):
		return '<User %r>' % self.username

	def __unicode__(self):
		return '<User %r>' % self.username 

# 匿名用户		
class AnonymousUser(AnonymousUserMixin):
	def can(self,permissions):
		return False 

	def	is_administrator(self):
		return False 

# 将其设为用户未登陆时的current_user的值		
login_manager.anonymous_user = AnonymousUser 

# flask-login必须实现，加载用户的回调函数
# 加载用户的回调函数接收以Unicode字符串形式表示的用户标识符
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# 分类		
class Category(db.Model):
	__tablename__ = 'categorys'

	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	
	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

	# 返回用户分类对应的博客文章列表	
	def get_posts_length(self,username):
		if username:
			return len(self.posts.filter_by(author=User.query.filter_by(username=username).first_or_404()).all())
		else:
			return len(self.posts.all())

	def __repr__(self):
		return '<Category %r>' % self.name

	def __unicode__(self):
		return self.name 
		
# 标签
class Tag(db.Model):
	__tablename__ = 'tags'

	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64))
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

	def get_id(self):
		return self.id

	def get_name(self):
		return self.name

	def __repr__(self):
		return '<Tag %r>' % self.name
	
	def __unicode__(self):
		return self.name 

# 标签和文章的关联表		
PostTag = db.Table('posts_tags',
	db.Column('tag_id',db.Integer,db.ForeignKey('tags.id')),
	db.Column('post_id',db.Integer,db.ForeignKey('posts.id'))
)

# 文章模型	
class Post(db.Model):
	__tablename__ = 'posts'
	__searchable__ = ['title','content']
	__analyzer__ = ChineseAnalyzer() 

	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(64)) # 标题
	content = db.Column(db.Text) # 内容
	fragment = db.Column(db.Text) # 内容片段，用于主页显示 
	viewcount = db.Column(db.Integer,default=0)
	create_time = db.Column(db.DateTime,index=True,default=datetime.utcnow) # 时间
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

	# 建立分类到文章的一对多关系
	category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
	category = db.relationship('Category',backref=db.backref('posts', lazy='dynamic'))

	# 建立标签到文章的多对多关系
	tags = db.relationship('Tag',
			secondary=PostTag,
			backref=db.backref('posts', lazy='dynamic'),lazy='dynamic')

	# 评论
	comments = db.relationship('Comment',backref='post',lazy='dynamic')

	def __repr__(self):
		return '<Post %r>' % self.title

	def __unicode__(self):
		return self.title 

	def get_id(self):
		return self.id

	def add_viewcount(self):
		self.viewcount +=1
		db.session.add(self)
		db.session.commit()

	#生成一批虚拟博客文章 		
	@staticmethod
	def generate_fake(count=100):
		from random import seed, randint
		import forgery_py 

		seed() 
		user_count = User.query.count()
		for i in range(count):
			# 指定随机用户
			u = User.query.offset(randint(0,user_count-1)).first()
			p = Post(content=forgery_py.lorem_ipsum.sentences(randint(1, 5)),
					create_time=forgery_py.date.date(True),
					author=u)
			db.session.add(p)
			db.session.commit() 

	# 删除所有博客文章
	@staticmethod	
	def delete_allpost():
		posts = Post.query.all() 
		for post in posts:
			db.session.delete(post)
			db.session.commit() 		

	# 根据博客正文内容，截取前200个字符给摘要字段
	@staticmethod
	def gen_fragment(content, size=200):
		tree = html.fromstring('<div>'+content+'</div>')
		node = tree.xpath('.')[0]
		text = re.sub(ur'\s+', ' ', node.text_content()).strip()
		return text[:size]

class Comment(db.Model):
	__tablename__ = 'comments'
	id = db.Column(db.Integer,primary_key=True)
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
	author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
	post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))


		
