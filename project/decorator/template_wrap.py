#-*- coding:utf-8 -*- 
@app.route('/')
def index():
	return render_template('index.html',value=42)

@app.route('/')
@templated('index.html')
def index():
	return dict(value=42)

@app.route('/')	
@template()
def index():
	return dict(value=42)

# 模板装饰器
from functools import wraps 
from flask import request 

def templated(template=None):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args,**kwargs):
			template_name = template 
			if template_name is None:
				template_name = request.endpoint \
								.replace（'.','/'）+'html'
			ctx = f(*args,**kwargs)
			if ctx is None:
				ctx = {}
			elif not isinstance(ctx,dict)
				return ctx 

			return render_template(template_name,**ctx)
		return decorated_function
	return decorator 


