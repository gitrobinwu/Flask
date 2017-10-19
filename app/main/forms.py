#-*- coding:utf-8 -*- 
from flask_login import current_user 
from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,BooleanField,SelectField
from flask_wtf.file import FileField,FileAllowed, FileRequired
from wtforms.validators import Length,DataRequired,Email,Regexp  
from wtforms import ValidationError
from ..models import Role,User,Post,Category,Tag
from flaskckeditor import CKEditor

# 普通用户资料表单,所有字段是可选的
class EditProfileForm(FlaskForm):
	name = StringField(label=u'真实姓名',validators=[Length(0,64)])
	location = StringField(label=u'地址',validators=[Length(0,64)])
	about_me = TextAreaField(label=u'自我描述')
	avatar = FileField(u'头像',validators=[
			FileRequired(),
			FileAllowed(['jpg','png','jpeg','gif'], u'仅允许上传图片类型文件!')
		])	
	submit = SubmitField(label=u'提交')


# 管理员使用的资料编辑表单 
class EditProfileAdminForm(FlaskForm):
	email = StringField(label=u'邮箱', validators=[DataRequired(), Length(1, 64),Email()])
	username = StringField(label=u'用户名', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,u'用户名只能包含字母、数字、下划线和点号')])
	confirmed = BooleanField(label=u'确认')
	role = SelectField(label=u'角色',coerce=int)

	name = StringField(label=u'真实姓名',validators=[Length(0,64)])
	location = StringField(label=u'地址',validators=[Length(0,64)])
	about_me = TextAreaField(label=u'自我描述')
	avatar = FileField(u'头像',validators=[
			FileRequired(),
			FileAllowed(['jpg','png','jpeg','gif'], u'仅允许上传图片类型文件!')
		])	
	submit = SubmitField(label=u'提交')

	# 初始化时要对role的下拉列表进行填充值 
	def __init__(self,user,*args,**kwargs):
		super(EditProfileAdminForm,self).__init__(*args,**kwargs)
		# 可选角色列表
		self.role.choices = [(role.id,role.name)
							 for role in Role.query.order_by(Role.name).all()]
		# 要编辑的用户					 
		self.user = user 

	# 判断是否和其他用户邮箱冲突	
	def validate_email(self,field):
		if field.data != self.user.email and \
				User.query.filter_by(email=field.data).first():
			raise ValidationError(u'改邮箱已经注册')
	
	# 判断是否和其他用户的用户名冲突
	def validate_username(self,field):
		if field.data != self.user.username and \
				User.query.filter_by(username=field.data).first():
			raise ValidationError(u'用户名已经被使用')

# 博客文章表单
class PostForm(FlaskForm):		
	title = StringField(label=u'博客标题',validators=[DataRequired()])
	body = TextAreaField(label=u'博客内容',validators=[DataRequired()])
	submit = SubmitField(label=u'提交')

# 分类	
class CategoryFrom(FlaskForm):
	category_name = StringField(label=u"分类名称",validators=[DataRequired(),Length(1,64)])

# 标签	
class TagForm(FlaskForm):
	tag_name = StringField(label=u"标签名称",validators=[DataRequired(),Length(1,64)])

# 博客文章表单
class CKEditorPostForm(FlaskForm,CKEditor):
	title = StringField(label=u'标题',validators=[DataRequired()])
	# 非必须
	summary = TextAreaField(label=u'摘要')
	category = SelectField(label=u'分类') 
	tag = SelectField(label=u'标签')
	ckhtml = TextAreaField(label=u'内容',validators=[DataRequired()])
	submit = SubmitField(label=u'提交')	
	
	def __init__(self,username,*args,**kwargs):
		super(CKEditorPostForm,self).__init__(*args,**kwargs)
		if username:
			# 从分类模型中加载初始选项
			self.category.choices = [ (category.id,category.name)
								 for category in Category.query.filter_by(author=User.query.filter_by(username=username).first_or_404()).order_by(Category.id.asc()).all() ]
			self.tag.choices = [ (tag.id,tag.name)
								 for tag in Tag.query.filter_by(author=User.query.filter_by(username=username).first_or_404()).order_by(Tag.id.asc()).all() ]
		else:
			self.category.choices = []
			self.tag.choices = []


	
