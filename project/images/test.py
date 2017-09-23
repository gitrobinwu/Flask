#-*- coding:utf-8 -*-
import urllib,hashlib

#Set your varibels here 
email = "694380339@qq.com"
default = "http://180.153.64.131:5008/static/1.jpg"
size = 40
# construct the url
gravatar_url = "https://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
gravatar_url += urllib.urlencode({'d':default, 's':str(size)})

if __name__ == '__main__':
	print gravatar_url 

