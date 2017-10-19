#-*- coding:utf-8 -*- 
from flask import render_template,redirect, url_for,flash,current_app,request,abort
from flask import jsonify
from flask_login import login_required,current_user 
from . import main
from .. import db
from ..models import User,Role,Permission,Post,Category,Tag
from .forms import EditProfileForm,EditProfileAdminForm,PostForm,CKEditorPostForm,CategoryFrom,TagForm
from ..decorators import admin_required 
from sqlalchemy import or_
from sqlalchemy import and_

# 用户个人站点 
# http://10.0.1.161:5008/?username=robin

# 首页-->处理博客文章
@main.route('/', methods=['GET'])
def index():
	page = request.args.get('page',1,type=int) # type=int 保证参数无法转换成整数时，返回默认值。

	username = request.args.get('username',None)
	print 'username ================ ',username
	if username:
		# 如果查询字符串中用户名非空，返回用户个人站点
		user = User.query.filter_by(username=username).first_or_404()
		pagination = user.posts.order_by(Post.create_time.desc()).paginate(
				page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
				error_out=False)
	else:
		#按时间排序返回博客文章
		pagination = Post.query.order_by(Post.create_time.desc()).paginate(
				page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
				error_out=False) # error_out=True页数超出范围返回404错误,False返回空列表
	
	# 返回当前分页记录
	posts = pagination.items

	# 增加分类索引
	categorys = Category.query.order_by(Category.name.asc()).all()
	
	# 增加最新文章列表
	latest_posts = Post.query.order_by(Post.create_time.desc()).limit(10).all()

	# 增加标签集合
	tags = Tag.query.all()
	
	# 非全文查看状态
	return render_template('index.html',onepost=False,posts=posts,
							pagination=pagination,categorys=categorys,latest_posts=latest_posts,tags=tags)

# 写博客
# 添加标签和分类
@main.route('/write-post',methods=['GET','POST'])
@login_required 
def write_post():
	category_form = CategoryFrom()
	tag_form = TagForm()

	form = CKEditorPostForm()	
	# 检查用户是否有写博客权限
	if current_user.can(Permission.WRITE_ARTICLES) and \
		request.method=="POST":
		print '-'*60
		print 'title = ',request.values.get('title')
		print 'summary = ',request.values.get('summary')
		print 'category = ',request.values.get('category')
		print 'tag = ',request.values.getlist('tag')
		print 'ckhtml = ',request.values.get('ckhtml')
		print '-'*60
		# 摘要不是必须的；如果用户没有输入摘要，那么就截取正文的前200个字符给摘要字段
		if form.summary.data:
			fragment = form.summary.data 
		else:
			fragment = Post.gen_fragment(form.ckhtml.data)
		'''
		title =  dsd
		summary =  
		category =  Python
		tag =  [u'Python,numpy,scipy,flask']
		ckhtml =  dsads
		'''
		# 分类(必选)
		category = Category.query.filter_by(name=request.values.get('category')).first()

		# 标签(可选)
		tag = request.values.getlist('tag')[0].encode('utf-8')
		print category,tag
		if tag:
			tags = list()
			for tag_name in tag.split(','):
				tag_obj = Tag.query.filter_by(name=tag_name).first()
				if tag_obj not in tags:
					tags.append(tag_obj)		
			post = Post(title=form.title.data,content=form.ckhtml.data,fragment=fragment+' ...',
				author=current_user._get_current_object(),category=category,tags=tags)
		else:
			post = Post(title=form.title.data,content=form.ckhtml.data,fragment=fragment+' ...',
				author=current_user._get_current_object(),category=category,tags=[])

		db.session.add(post)
		db.session.commit()
		return jsonify(id=post.get_id())

	return render_template('write_post.html',form=form,category_form=category_form,tag_form=tag_form)	

# 上传文件或者图片
@main.route('/ckupload/',methods=['GET','POST'])
def ckupload():
	form = CKEditorPostForm()
	return form.upload(endpoint=current_app)
	
# 关于我	
@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	# 返回当前用户的博客文章列表
	page = request.args.get('page', 1, type=int)
	pagination = user.posts.order_by(Post.create_time.desc()).paginate(
			page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
			error_out=False)
	
	# 返回当前分页记录
	posts = pagination.items
	# 非全文查看状态
	return render_template('user.html',user=user,onepost=False,posts=posts,
							pagination=pagination)
	
# 用户个人资料编辑	
@main.route('/edit-profile',methods=['GET','POST'])
@login_required 
def edit_profile():
	form = EditProfileForm() 
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.about_me = form.about_me.data

		# 新增提交用户头像
		avatar = request.files['avatar']
		filename = avatar.filename
		# 上传路径
		UPLOAD_FOLDER = current_app.static_folder+'/'+'avatar/'
		filepath = u"{0}{1}_{2}".format(UPLOAD_FOLDER,current_user.username,filename)
		avatar.save(filepath)
		staticfile = u'/static/avatar/{0}_{1}'.format(current_user.username,filename)
		current_user.real_avatar = staticfile
		db.session.add(current_user)
		flash(u'您的个人信息已经更新')
		return redirect(url_for('main.user',username=current_user.username)) # 更新个人资料
	form.name.data = current_user.name 
	form.location.data = current_user.location 
	form.about_me.data = current_user.about_me 
	return render_template('edit_profile.html',form=form)


# 管理员资料编辑
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data 
		user.username = form.username.data 
		user.confirmed = form.confirmed.data 
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data 
		user.location = form.location.data 
		user.about_me = form.about_me.data 

		# 新增提交用户头像
		avatar = request.files['avatar']
		filename = avatar.filename
		# 上传路径
		UPLOAD_FOLDER = current_app.static_folder+'/'+'avatar/'
		filepath = u"{0}{1}_{2}".format(UPLOAD_FOLDER,user.username,filename)
		avatar.save(filepath)
		staticfile = u'/static/avatar/{0}_{1}'.format(user.username,filename)
		user.real_avatar = staticfile
		db.session.add(user)
		flash(u'该用户的信息已经更新了')
		return redirect(url_for('.user',username=user.username))
	form.email.data = user.email 
	form.username.data = user.confirmed
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id 
	form.name.data = user.name 
	form.location.data = user.location
	form.about_me.data = user.about_me 
	return render_template('edit_profile.html',form=form)

# 文章的固定链接
@main.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)

	# 增加分类索引
	categorys = Category.query.order_by(Category.name.asc()).all()
	
	# 增加最新文章列表
	latest_posts = Post.query.order_by(Post.create_time.desc()).limit(10).all()

	# 增加标签集合
	tags = Tag.query.all()

	# 全文查看状态
	return render_template('post.html',onepost=True,post=post,posts=[post],
			categorys=categorys,latest_posts=latest_posts,tags=tags)

# 编辑文章
@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	# 不是管理员或者文章作者返回403 
	if current_user != post.author and \
			not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = CKEditorPostForm()
	#if form.validate_on_submit():
	if request.method=="POST":
		post.title= form.title.data 
		post.content = form.ckhtml.data
		print "In edit-post category = ",request.values.get('category')
		print "In edit-post tags = ",request.values.getlist('tag')
		'''
		In edit-post category =  3
		In edit-post tags =  [u'4', u'5']
		'''
		# 更新摘要
		if form.summary.data:
			post.fragment = form.summary.data +' ...'
		else:
			post.fragment = Post.gen_fragment(form.ckhtml.data)+' ...'
		
		# 更新标签列表	
		ids = request.values.getlist('tag')
		if ids:
			tags = list()
			for id in ids:
				id = int(id.encode('utf-8'))
				tag_obj = Tag.query.get(id) 
				if tag_obj not in tags:
					tags.append(tag_obj)
			post.tags = tags		
		else:
			# 清空标签
			post.tags = []

		# 更新类别
		category_id = request.values.get('category')
		post.category = Category.query.get(category_id)

		db.session.add(post)
		flash(u'文章已经被更新')
		return redirect(url_for('.post', id=post.id))
	form.title.data = post.title
	form.summary.data = post.fragment
	form.ckhtml.data = post.content 
	category = post.category
	tag_ids = list()
	for tag in post.tags:
		if tag.id not in tag_ids: 
			tag_ids.append(str(tag.id))
	return render_template('edit_post.html',post=post,form=form,category=category,tag_ids=','.join(tag_ids))

# 搜索视图函数
@main.route('/search',methods=['GET','POST'])
def search():
	# 获取查询关键字，之所以重定向，防止用户刷新表单重复提交
	if request.method == 'POST':
		return redirect(url_for('.search_results',keyword=request.form['keyword']))		
	return redirect(url_for('.index'))

# 搜索结果页
@main.route('/search_results/<keyword>')
def search_results(keyword):
	# 查询标题或者内容包含查询关键字的文章
	print '-'*30+'results of '+keyword+'-'*30
	page = request.args.get('page',1,type=int) # type=int 保证参数无法转换成整数时，返回默认值。

	pagination = Post.query.\
				 whoosh_search(keyword).\
				 order_by(Post.create_time.desc()).paginate(
						 page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
						 error_out=False)
	
	# 返回当前分页记录
	posts = pagination.items

	# 增加分类索引
	categorys = Category.query.order_by(Category.name.asc()).all()

	# 增加最新文章列表
	latest_posts = Post.query.order_by(Post.create_time.desc()).limit(10).all()

	# 增加标签集合
	tags = Tag.query.all()

	# 列表形式显示文章-->只显示摘要
	return render_template('search_results.html',query=keyword,onepost=False,posts=posts,
							pagination=pagination,categorys=categorys,latest_posts=latest_posts,tags=tags)


# 添加分类
@main.route('/new_category',methods=['GET','POST'])
@login_required
def new_category():
	if request.method=="POST":
		print 'category_name = ',request.values.get('category_name')
		# 新建分类
		category = Category(name=request.values.get('category_name'))
		db.session.add(category)
		db.session.commit()
		return jsonify(id=category.get_id(),name=category.get_name())
	return redirect(url_for('.write_post'))

# 添加标签
@main.route('/new_tag',methods=['GET','POST'])
@login_required
def new_tag():
	if request.method=="POST":
		print 'tag_name = ',request.values.get('tag_name')
		# 新建标签
		tag = Tag(name=request.values.get('tag_name'))
		db.session.add(tag)
		db.session.commit()
		return jsonify(id=tag.get_id(),name=tag.get_name())
	return redirect(url_for('.write_post'))

# 分类路由	
@main.route('/category/<name>')
def category(name):
	print "category =============== ",name;
	#按时间排序返回博客文章
	page = request.args.get('page',1,type=int) # type=int 保证参数无法转换成整数时，返回默认值。
	category = Category.query.filter_by(name=name).first()
	pagination = category.posts.order_by(Post.create_time.desc()).paginate(
			page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
			error_out=False) # error_out=True页数超出范围返回404错误,False返回空列表
	
	# 返回当前分页记录
	posts = pagination.items

	# 增加分类索引
	categorys = Category.query.order_by(Category.name.asc()).all()
	
	# 增加最新文章列表
	latest_posts = Post.query.order_by(Post.create_time.desc()).limit(10).all()

	# 增加标签集合
	tags = Tag.query.all()

	# 非全文查看状态
	return render_template('category.html',name=name,onepost=False,posts=posts,
							pagination=pagination,categorys=categorys,latest_posts=latest_posts,tags=tags)

# 标签路由
@main.route('/tag/<name>')
def tag(name):
	print "tag ================ ",name
	#按时间排序返回博客文章
	page = request.args.get('page',1,type=int) # type=int 保证参数无法转换成整数时，返回默认值。
	tag = Tag.query.filter_by(name=name).first()
	pagination = tag.posts.order_by(Post.create_time.desc()).paginate(
			page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
			error_out=False) # error_out=True页数超出范围返回404错误,False返回空列表

	# 返回当前分页记录
	posts = pagination.items

	# 增加分类索引
	categorys = Category.query.order_by(Category.name.asc()).all()
	
	# 增加最新文章列表
	latest_posts = Post.query.order_by(Post.create_time.desc()).limit(10).all()

	# 增加标签集合
	tags = Tag.query.all()

	# 非全文查看状态
	return render_template('tag.html',name=name,onepost=False,posts=posts,
							pagination=pagination,categorys=categorys,latest_posts=latest_posts,tags=tags)



