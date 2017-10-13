#-*- coding:utf-8 -*- 
import os 
import datetime 
import random 
from flask import Flask,request,render_template,url_for,make_response,redirect

app = Flask(__name__)

# 生成随机文件名字	当前时间+随机数
def gen_rnd_filename():
	filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))

# 首页路由	
@app.route('/',methods=['GET','POST'])
def index():
	if request.method == "POST":
		print '-'*60
		print request.form['ckeditor'] 
		print '-'*60
		redirect(url_for('index'))
	return render_template('index.html')


# 上传	
@app.route('/ckupload', methods=['GET','POST'])
def ckupload():
	"""CKEditor file upload"""
	error = ''
	url = ''
	callback = request.args.get("CKEditorFuncNum")

	# ImmutableMultiDict([('langCode', u'zh-cn'), ('CKEditor', u'editor'), ('CKEditorFuncNum', u'0')])   
	print request.args 
	# ImmutableMultiDict([('upload', <FileStorage: u'echars.html' ('text/html')>)])
	print request.files 
	if request.method == 'POST' and 'upload' in request.files:
		fileobj = request.files['upload']
		fname, fext = os.path.splitext(fileobj.filename)
		rnd_name = '%s%s' % (gen_rnd_filename(), fext)

		# 保存上传文件的路径
		filepath = os.path.join(app.static_folder, 'upload', rnd_name)

		# 检查路径是否存在，不存在则创建
		dirname = os.path.dirname(filepath)
		if not os.path.exists(dirname):
			try:
				os.makedirs(dirname)
			except:
				error = 'ERROR_CREATE_DIR'
		elif not os.access(dirname, os.W_OK):
			error = 'ERROR_DIR_NOT_WRITEABLE'

		if not error:
			fileobj.save(filepath)
			url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
	else:
		error = 'post error'

	# CKEditorFuncNum : 回调函数序号。CKEditor通过URL参数提交给服务端
	# URL : 上传后文件的URL
	# Error : 错误信息。若无错误，返回空字符串 
	# 若无错误，回调函数将返回的URL转交给CKEditor处理	
	res = """
		<script type="text/javascript">
			window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
		</script>""" % (callback, url, error)

	response = make_response(res)
	response.headers["Content-Type"] = "text/html"
	return response

if __name__ == '__main__':
	#print app.static_folder
	app.run(host='0.0.0.0',port=5010)
	

