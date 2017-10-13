#-*- coding:utf-8 -*- 
# Restful And 日志
from flask import Flask 
from flask_restful import Resource,Api
import logging

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
	def get(self):
		app.logger.info('this is a string')
		app.logger.debug('A value for debugging')
		app.logger.warning('A warning occurred (%d apples)',42)
		app.logger.error('An error occurred')

		return {'hello':'world'}

api.add_resource(HelloWorld,'/')

if __name__ == '__main__':
	handler = logging.FileHandler('flask4.log',encoding='UTF-8')
	handler.setLevel(logging.DEBUG) #Error Warning 
	logging_format = logging.Formatter(
		'%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')	
	handler.setFormatter(logging_format)

	app.logger.addHandler(handler)
	app.run(host='0.0.0.0',port=5008)





