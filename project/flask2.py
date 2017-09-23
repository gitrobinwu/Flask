#-*- coding:utf-8 -*- 
1, HTTP方法
HTTP(与web应用会话的协议)有许多不同的访问URL方法，默认情况下，路由只回应GET请求
但是通过route()装饰器传递methods参数可以改变这个行为.
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		do_the_login()
	else:
		show_the_login_form() 

2,静态文件
动态web应用也会需要静态文件，通常是CSS和JavaScript文件。理想情况下，已经配置好Web服务器来提供静态文件。Flask在包中或者模块所在目录中创建一个名为static的文件夹.

# 给静态文件生成URL，使用特殊的'static'端点名:
url_for('static',filename='style.css')
# static/style.css

3,模板渲染
# render_template() 方法来渲染模板

4, 访问请求数据
对于web应用，与客户端发送给服务器的数据交互至关重要。在Flask中由全局的request对象来提供这些信息.
之所以能保证线程安全，是因为环境作用域

# 环境局部变量
# 绑定当前的应用和WSGI环境到那个环境上(线程)，能保证一个应用调用另一个应用时不会出现问题。

# 利用环境局部变量实现自动化测试
# 将一个请求对象绑定到环境
# 单元测试最简单的解决方案是: 用test_request_context() 环境管理器。
# 结合with声明，绑定一个测试请求

5, 请求对象
from flask import request 
#1, 当前请求的HTTP方法可通过method属性来访问
#2, 通过attr~flask.request.form属性来访问表单数据(POST或者PUT请求提交的数据)
@app.route('/login',methods=['POST','GET'])
def login():
	error = None 
	if request.method == 'POST':
		if valid_login(request.form['username'],
				request.form['password']):
			return log_the_user_in(request.form['username'])
		else:
			error = 'Invalid username/password'
	return render_template('login.html',error=error)

# 当访问form属性中的不存在的键时，会抛出一个KeyError错误，一般不用处理
	 
#3, 可通过args属性来访问URL中提交的参数(?key=value)
searchword = request.args.get('q','')	
# 推荐用get来访问URL参数或捕获KeyError,因为用户可能会修改URL，向他们展现一个400 bad request页面影响用户体验

6,文件上传
# 确保你没忘记在 HTML 表单中设置 enctype="multipart/form-data" 属性，不然你的浏览器根本不会发送文件
已上传的文件存储在内存或者是文件系统中的一个临时位置。可以通过请求对象的files属性访问它们。每个上传的文件都会存储在这个字典里，表现为一个Python file对象。还有一个save()方法，这个方法允许把文件保存到服务器的文件系统上。 

form flask import request 
@app.route('/upload',methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['the_file']
		f.save('/var/www/uploads/uploaded_file.txt')

# 如果想知道上传文件在客户端的文件名是什么，可以访问filename属性
from flask import request 
from werkzeug import secure_filename 
@app.route('/upload',methods=['GET','POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['the_file']
		f.save('/var/www/uploads/'+secure_filename(f.filename))

7, Cookies 
# 可通过cookies属性来访问Cookies,用响应对象的set_cookie方法来设置Cookies。
# 请求对象的cookies属性是一个内容为客户端提交的所有Cookies的字典
# 如果想使用会话，请不要直接使用Cookies 

#1, 读取cookies 
from flask import request 
@app.route('/')
def index():
	# 获取存储在客户端的Cookies 
	username = request.cookies.get('username')

#2, 存储cookies 
from flask import make_response 
@app.route('/')
def index():
	response = make_response(render_template(...))
	response.set_cookie('username','the username')
	return response

# 可注意到，Cookies是设置在响应对象上的。由于通常视图函数只是返回字符串，之后Flask将字符串转换为响应对象。	
# 如果要显示地转换，可以使用make_response()函数后再进行修改.
# 有时想设置Cookie，但响应对象不能存在，可以利用延迟请求回调。

#3, flask.make_response(*args)	--> API 
def index():
	return render_template('index.html',foo=42)
# you can now do something like this:
def index():
	response = make_response(render_template('index.html',foo=42))
	response.headers['X-Parachutes'] = 'parachutes are cool'
	return response 

# This for example creates a response with a 404 error code 
response = make_response(render_template('not_found.html'),404)

response = make_response(view_function())
response.headers['X-Parachutes'] = 'parachutes are cool'

8, 重定向和错误
# redirect()函数把用户重定向到其它地方
# abort() 放弃请求并返回错误代码

from flask import abort,redirect,url_for 
@app.route('/')
def index():
	return redirect(url_for('login'))

@app.route('/login')
def login():
	abort(401)
	this_is_never_executed() 
# 这是一个相当于无意义的例子因为用户会从主页重定向到一个不能访问的页面(401意味着禁止访问)
# 但是它展示了重定向是如何工作的。

# 默认情况下，错误代码会显示一个黑白的错误页面。如果你要定制错误页面，可以使用errorhandler()装饰器
from flask import render_template 

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'),404 
# 注意render_template()调用之后的404。这告诉Flask,该页的错误代码是404,即没有找到。默认为200，也就是一切正常。 

9,关于响应
# 视图函数的返回值会被自动转换为一个响应对象。如果返回值是一个字符串，它被转换为该字符串为主体的，状态码为200 OK的，MIME类型是"text/html"的响应对象。 

#1，如果返回的是一个合法的响应对象，会从视图直接返回。
#2, 如果返回的是一个字符串，响应对象会用字符串数据和默认参数创建。
#3, 如果返回的是一个元组，且元组中的元素可以提供额外的信息。这样的元组必须是(response,status,headers)的形式，且至少包含一个元素。status值会覆盖状态代码，headers可以是一个列表或字典，作为额外的消息标志值。

@app.errorhandler(404)
def not_found(error):
	response = make_response(render_template('error.html'),404)
	response.headers['X-Something'] = 'A value'
	return response 














	











	
















	













































































































