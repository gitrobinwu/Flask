#-*- coding:utf-8 -*- 
#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 创建程序实例
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
# 数据库迁移扩展	
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
# 为了可以使用数据库迁移命令，Flask-Migrate提供MigrateCommand类来连接Flask-Script的manager对象 
manager.add_command('db', MigrateCommand)

# 在数据库迁移可以维护之前，必须通过init命令来创建一个迁移库
# python hello.py db init  --> 

# 创建迁移脚本 --> 
# 在Alembic,数据库迁移工作由迁移脚本完成，这个脚本有两个函数，分别叫做upgrade()和downgrade()
# upgrade()函数实施数据库更改，是迁移的一部分，downgrade()函数则删除它们

# Alembic迁移可以分别使用revision和migrate命令手动或自动创建
# python hello.py db migrate -m "initial migration" //创建自动迁移脚本

# 更新数据库 --> 
# 一旦迁移脚本被审查且接受,就可以使用db upgrade命令更新到数据库中
# python hello.py db upgrade 

# 第一次迁移实际上相当于调用db.create_all() 
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
