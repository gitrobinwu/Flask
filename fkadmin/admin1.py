#-*- coding:utf-8 -*-
from flask import Flask,url_for 
from flask import render_template 
from flask_admin import Admin,BaseView,expose,AdminIndexView 
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form import SecureForm
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel 

import os 
from datetime import datetime 
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I hate flask, because it is awesome'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DETABASE_URI') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 设置成中文
app.config['BABEL_DEFAULT_LOCALE'] = 'zh_CN'

# 实例化admin类实例	
admin = Admin(
	app,
	"My APP",
	index_view=AdminIndexView( # 首页视图
		name=u'导航栏',
		template='welcome.html',
		url='/admin'
	),
	template_mode='bootstrap3',# 使用模式
)

db = SQLAlchemy(app)
babel = Babel(app)

# /admin/?lang=zh_CN	
@babel.localeselector
def get_locale():
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'en')

class BlogPost(db.Model):
	__tablename__ = 'blogposts'

	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(64))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # 时间戳

	def __init__(self,title,body):
		self.title = title 
		self.body = body 

	def __repr__(self):
		return '<Post %r>' % self.title 

# 如果在flask路由里面集成admin模板会报一下错误: 	
# UndefinedError: 'admin_base_template' is undefined
@app.route('/test')
def test():
	#return "hello world test"
	return render_template('flask_test.html')

# 一个关于管理视图的重要约束是每个视图类应该拥有一个默认的以根URL /开头的页面视图方法	
class MyView(BaseView):
	# /admin/myview/ 
	@expose('/')
	def index(self):
		# url = url_for('test') # 引用局部视图 --> /admin/myview/test1/
		url = url_for('testadmin1.index') # --> /admin/testadmin1/ 引用外部视图 
		print '--------------'+url+'----------------'
		return self.render('index.html',url=url)

	@expose('/test')
	def test(self):
		return self.render('test.html')

class TestAdmin(BaseView):
	# /admin/testadmin/
	@expose('/') 
	def index(self):
		return self.render('testadmin.html')

# 增加管理视图		
# BuildError: Could not build url for endpoint 'myview.test'. Did you mean 'myview.test1' instead		
# 将myview蓝本修改成testadmin蓝本绑定到MyView视图
# 单级菜单	
#add_view 相当于注册蓝本		
admin.add_view(MyView(name='Hello',endpoint='testadmin')) # --> /admin/testadmin/
admin.add_view(TestAdmin(name="TestAdmin",endpoint="testadmin1")) # testadmin-->testadmin1 

# 增加多级别的菜单项目
# category指定顶级菜单项目的名字，并且所有与之关联的视图，都会通过下拉菜单进入
# /admin/test2/
admin.add_view(MyView(name="Hello 1",endpoint="test1",category='Test')) # myview-->test1  
admin.add_view(MyView(name="Hello 2",endpoint='test2',category='Test')) # myview--> test2 

# 定制模型视图
class MyBlogPost(ModelView):
	# enabling csrf protection 
	form_base_class = SecureForm
	# 禁用模型创建功能
	can_create = False 
	
	# 该模型视图中需要显示的字段
	column_list = ('id','title','body','timestamp')
	column_labels = {
		'id': u'序号',
		'title': u'标题',
		'body': u'内容',
		'timestamp': u'发布时间'
	}
	
	# 添加要搜索的字段 
	column_searchable_list = ('title','body')
	# 字段格式化
	# column_formatters = dict(
	# 	body=lambda v, c, m, p: '**'+m.body[-6:],
	# )

	def __init__(self,session,**kwargs):
		super(MyBlogPost,self).__init__(BlogPost,session,**kwargs)

# 增加模型视图
admin.add_view(MyBlogPost(db.session,name=u"博客文件"))

# 增加文件管理
admin.add_view(FileAdmin(app.static_folder,name=u"管理文件"))

if __name__ == '__main__':
	'''db.drop_all()
	db.create_all()

	p1 = BlogPost(title="post1",body='my first post')
	p2 = BlogPost(title='post2',body='my second post')
	p3 = BlogPost(title='post3',body='my third and last post')
	db.session.add_all([p1,p2,p3])
	db.session.commit()'''
	
	# 静态路由文件
	#print app.static_folder
	app.run(host='0.0.0.0',port=5013)


	
