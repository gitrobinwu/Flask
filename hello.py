#-*- coding: utf-8 -*- 
from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required,DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

# validators 指定一个由验证函数组成的列表
# 第一个参数是把表单渲染成HTML 时使用的标号
class NameForm(FlaskForm):
	# StringField类表示属性为type="text"的<input>元素
    name = StringField('What is your name?', validators=[DataRequired()])
	# SubmitField类表示属性为type="submit"的<input>元素
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
		# 获取表单数据
        name = form.name.data
		# 清空表单数据
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


if __name__ == '__main__':
    manager.run()
