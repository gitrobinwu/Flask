#-*- coding:utf-8 -*- 
from lxml import html
import re

htmltext = u'''
	<div>
	<p>我爱中国<br />
	</p>

	<p>得不到的永远在骚动<br />
	我爱北京天安门<br />
	<br />
	这是一个测试</p>
	</div>
'''
def gen_summary(content,size=120):
	tree = html.fromstring(htmltext)
	node = tree.xpath('.')[0]
	text = re.sub(ur'\s+', ' ', node.text_content()).strip()
	return text[:size] + ' ...'

if __name__ == '__main__':
	print gen_summary(htmltext)


