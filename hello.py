#-*- coding:utf-8 -*- 
from flask import Flask
app = Flask(__name__)

#路由以及视图函数
# 静态URL 
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


# 动态URL 
# 路由中的动态部分默认使用字符串，不过也可使用类型定义。
#/user/<int:id> Flask在路由支持int,float,path 类型
# path类型也是字符串，但不把斜线视作分割符，而是将其作为动态片段的一部分
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5006,debug=True)
