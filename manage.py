""" 管理脚本 """

import os
from flask_script import Manager, Shell
from app import create_app

app = create_app(os.getenv('ENV'))

manager = Manager(app)


def make_shell_context():
    """ 生成manager相关shell内容 """
    return dict(app=app)


manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()