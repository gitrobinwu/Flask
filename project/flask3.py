#-*- coding:utf-8 -*-
1, 会话
#除了请求对象之外，还有一个session对象，允许在不同请求之间存储特定用户的信息。
# 它是在Cookies的基础上实现的，并且对Cookies进行密匙签名。意味着用户可以查看你的Cookies的内容，
# 但是不能修改它，除非用户知道签名的密匙

from flask import Flask,session,redirect,url_for,escape,request 
app = Flask(__name__)

@app.route('/')
def index():
	if 'username' in session:
		# escape 可以在模板引擎之外做转义
		return 'Logged in as %s' % escape(session['username'])
	return 'You are not logged in'

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	return '''
		<form action="" method="POST">
			<p><input type=text name=username>
			<p><input type=submit value=Login>
		</form>
	'''

@app.route('/login')
def logout():
	# remove the username from the session if it's there
	session.pop('username',None)
	return redirect(url_for('index'))

# set the secret .keep this really secret 
app.secret_ket = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'	

# 如何生成强壮的密匙
# 随机问题在于很难判断什么是真随机，一个密码是应该足够随机。操作系统可以基于一个密匙随机生成器来生成漂亮的随机值，这个值可以用来做密匙

# import os 
# os.urandom(24)

2, 消息闪现
# 反馈，是良好的应用和用户界面的重要构成。如果用户得不到足够的反馈，很可能开始厌恶这个应用。
# Flask 提供了消息闪现系统，可以简单地给用户反馈.消息闪现系统通常会在请求结束时记录信息,
# 并在下一个(且仅在下一个)请求中访问记录的信息。展现这些消息通常结合模板布局。


# 使用flash()方法可以闪现一条消息。要操作消息本身，使用get_flashed_message()函数，并且在模板中也可以使用。 



