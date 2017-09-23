#-*- coding:utf-8 -*-
from flask import Flask,flash,redirect,render_template,\
		 request,url_for 

# Flask提供一个非常简单方法来使用闪现系统向用户反馈信息。
# 闪现系统使得在一个请求结束的时候记录一个信息，然后在且仅仅在下一个请求中访问这个数据。
app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login',methods=['GET','POST'])	
def login():
	error = None 
	if request.method == "POST":
		if request.form['username'] != 'admin' or \
			request.form['password'] != 'secret':
			error = 'Invalid credentials'
		else:
			flash('You were successfully logged in')
			return redirect(url_for('index'))
	return render_template('login.html',error=error)	

if __name__ == "__main__":
	app.run(host="0.0.0.0",port=5008)


# 分类闪现
'''
当闪现一个消息时，可以提供一个分类。未指定分类时默认的分类为"message"。
可以使用分类来提供给用户更好的反馈，例如:错误信息应该被显示为红色北京
要使用一个自定义的分类，只要使用flush()函数的第二个参数:
	flash(u'Invalid password provided','error')
在模板中，可以调用get_flashed_messages()函数来返回这几个分类
'''





