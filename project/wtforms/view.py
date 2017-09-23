#-*- coding:utf-8 -*-

@app.route('/register',methods=['GET','POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User(form.username.data,form.email.data,
				form.password.data)
		db.session.add(user)
		flash('Thanks for registering')
		return redirect(url_for('login'))
	return render_template('register.html',form=form)

# 备忘表
'''
1, 如果数据是以POST方式提交的，那么基于请求的form属性的值创建表单。反过来，如果使用GET提交的，就从args属性创建
	searchword = request.args.get('q','')	
2, 验证表单数据，调用validate()方法。如果数据验证通过，此方法将会返回True,否则返回False 
3, 访问表单的单个值，使用form.<NAME>.data 	
'''
	
