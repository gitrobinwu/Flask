#-*- coding:utf-8 -*- 
import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required,DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
# 配置数据库URL
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 每次请求结束后，自动提交数据库的变动	
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
#db 对象是SQLAlchemy 类的实例，表示程序使用的数据库 
db = SQLAlchemy(app)

# 常用的SQLAlchemy列选项
# primary_key 如果设为True,这列就是表的主键
# unique True,这列不允许出现重复的值
# index True 为这列创建索引，提升查询效率
# nullable True 这列允许使用空值；如果设为False,这列不允许使用空值
# default 为这列定义默认值	
class Role(db.Model):
	# 类变量__tablename__定义在数据库中使用的表名 
    __tablename__ = 'roles'
	# db.Column类构造函数第一个参数是数据库列和模型的类型
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
	# users属性代表这个关系面向对象视角
	# 对于一个Role类的实例，其users属性将返回与角色相关联的用户组成的列表
	# db.relationship()第一个参数表明这个关系的另一端是哪个模型。

	# 关系选项
	# backref 在关系的另一个模型中添加反向引用
	# uselist 如果设为Fales，不使用列表，而使用标量值
	# 大多数情况下，db.relationship()都能自行找到关系中的外键 
	# primaryjoin 明确指定两个模型之间使用的联结条件。只在模棱两可的关系中需要指定
	# lazy 指定如何加载相关记录 dynamic（不加载记录，但提供加载记录的查询）
    users = db.relationship('User', backref='role', lazy='dynamic')
	
	# 一对多关系表示，但调用db.relationship() 时要把uselist 设为False，把“多”变成“一”。
	# 多对一关系也可使用一对多表示，对调两个表即可
    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
	# 定义外键
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


if __name__ == '__main__':
    db.create_all()
    manager.run()
