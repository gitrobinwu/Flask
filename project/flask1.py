#-*- coding:utf-8 -*- 
from flask import Flask,url_for,render_template,request
# url_for url构建
# render_template 模板渲染
# request对象 --> 访问请求数据
app = Flask(__name__)

@app.route('/hello/')	
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html',name=name)
# Flask会在templates文件夹里寻找模板。所以，如果你的应用是个模块，这个文件夹应该与模块同级;如果是一个包，那么这个文件夹作为包的子目录。 
	
@app.route('/')
def hello_world():
	return 'Hello World!'

# 变量规则
# <variable_name>
# <converter:variable_name>
@app.route('/user/<username>')
def show_user_profile(username):
	# show the user profile for that user 
	return 'User %s' % username 

# 给变量添加转换器	
@app.route('/post/<int:post_id>')
def show_post(post_id):
	# show the post with the given id,the id is an integer
	return 'Post %d' % post_id 
# 转换器: 
# int: 接受整数 
# float: 同int,但是接受浮点数
# path: 和默认的相似，但也接受斜线

# 访问一个结尾不带斜线的URL会被Flask重定向到带斜线的规范URL去	
@app.route('/login')
def login():pass

if __name__ == '__main__':
# 构造URL
# 可以用url_for()来给指定的函数构造URL.接受函数名作为第一个参数，也接受对应URL规则的变量部分的命名参数。未知变量会添加到URL末尾作为查询参数.
	with app.test_request_context():
		print url_for('hello_world')
		print url_for('login')
		print url_for('login',next='/')
		print url_for('show_user_profile',username='John Doe')
	
	# 将请求对象绑定到环境 --> 单元测试 
	with app.test_request_context('/hello',method='POST'):
		print request.path
		print request.method
	
	print '-'*60 
	app.run(host='0.0.0.0',port=5006)

# 为什么要构建URL而非在模板中硬编码 
#1, 反向构建通常比硬编码的描述性更好。更重要的是,它允许你一次性修改URL,而不是到处边找边改 
#2, URL构建会转义特殊字符和Unicode数据
#3, 如果应用不位于URL的根路径，url_for()会妥善处理这个问题

	





