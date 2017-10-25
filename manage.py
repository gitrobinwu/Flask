#-*- coding:utf-8 -*-
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role,Post,Permission,Category,Tag,PostTag,Comment
from flask_script import Manager, Shell,Server
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	"""自动加载环境"""
	return dict(
			app=app, 
			db=db, 
			User=User, 
			Role=Role,
			Post=Post,
			Category=Category,
			Tag=Tag,
			PostTag=PostTag,
			Comment=Comment,
			Permission=Permission,
		)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver',
		Server(host='0.0.0.0',port=5008))

@manager.command
def database_init():
	"""初始化数据库表环境"""
	db.drop_all()
	db.create_all()
	Role.insert_roles()

@manager.command
def admin():
	"""add administrator"""
	from getpass import getpass
	username = raw_input("\_admin username: ")
	email = raw_input("\_admin email: ")
	password = getpass("\_admin password: ")
	u = User(
		email = email,
		username = username,
		password = password,
		role = Role.query.get(2),
		confirmed = True
	)
	db.session.add(u)
	db.session.commit()
	print "<admin user %s add in database>" % username

@manager.command 
def adduser():
	"""add user"""
	from getpass import getpass
	username = raw_input("\_username: ") 
	email = raw_input("\_email: ")
	role_id = raw_input("\_[1:moderator 2:admin 3:user]: ")
	password = getpass("\_password: ")
	u = User(
		email = email,
		username = username,
		password = password,
		role_id = role_id,
		confirmed = True
	)
	db.session.add(u)
	db.session.commit()
	print "<user %s add in database>" % username 

if __name__ == '__main__':
    manager.run()


