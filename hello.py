from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# 程序可以把数据存储在用户会话中，在请求之间“记住”数据
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
		# 从form.name.data获取用户输入，一旦请求结束，数据就丢失了
		# 因为这个POST 请求使用重定向处理，所以程序需要保存输入的名字
		#这样重定向后的请求才能获得并使用这个名字，从而构建真正的响应
        session['name'] = form.name.data
        return redirect(url_for('index'))
	# session.get('name')直接从会话中读取name参数的值，对于不存在的键返回None
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    manager.run()
