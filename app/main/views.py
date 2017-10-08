#-*- coding:utf-8 -*- 
from flask import render_template,redirect, url_for,flash,current_app,request,abort
from flask_login import login_required,current_user 
from . import main
from .. import db
from ..models import User,Role,Permission,Post 
from .forms import EditProfileForm,EditProfileAdminForm,PostForm,CKEditorPostForm
from ..decorators import admin_required 

# 首页-->处理博客文章
@main.route('/', methods=['GET', 'POST'])
def index():
	#按时间排序返回博客文章
	page = request.args.get('page',1,type=int) # type=int 保证参数无法转换成整数时，返回默认值。
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
			page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
			error_out=False) # error_out=True页数超出范围返回404错误,False返回空列表
	
	# 返回当前分页记录
	posts = pagination.items
	# 非全文查看状态
	return render_template('index.html',onepost=False,posts=posts,
							pagination=pagination)
# 写博客
@main.route('/write-post',methods=['GET','POST'])
def write_post():
	form = CKEditorPostForm()	
	# 检查用户是否有写博客权限
	if current_user.can(Permission.WRITE_ARTICLES) and \
		form.validate_on_submit():
		post = Post(title=form.title.data,body=form.ckhtml.data,
				author=current_user._get_current_object())
		db.session.add(post)
		return redirect(url_for('main.index'))
	return render_template('write_post.html',form=form)	

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
	pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
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
	# 全文查看状态
	return render_template('post.html',onepost=True,post=post,posts=[post])


# 编辑文章
@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
	post = Post.query.get_or_404(id)
	# 不是管理员或者文章作者返回403 
	if current_user != post.author and \
			not current_user.can(Permission.ADMINISTER):
		abort(403)
	form = PostForm() 
	if form.validate_on_submit():
		post.title= form.title.data 
		post.body = form.body.data
		db.session.add(post)
		flash(u'文章已经被更新')
		return redirect(url_for('.post', id=post.id))
	form.title.data = post.title
	form.body.data = post.body 
	return render_template('edit_post.html',form=form)


