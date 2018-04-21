""" 初始化构建应用 """

import os
import getpass
import shutil
import subprocess
import random, string
import time

cwd = os.getcwd()
cur_dir = cwd.split('/')[-1]
user = getpass.getuser()

# 开始
print('Starting deploy...')

# 初始化pipenv
print('初始化pipenv')

status, output = subprocess.getstatusoutput('pipenv install')

if status == 0:
    # 获取venv路径
    status, output = subprocess.getstatusoutput('pipenv --venv')

    if status == 0:
        venv = output
        print('成功! venv: %s' % venv)
    else:
        venv = None
        print('失败: %s' % output)
else:
    print('失败: %s' % output)


# 开始生成各种文件
def create_file(filename, resouce):
    """ 封装写文件 """
    with open(filename, 'w') as f:
        f.writelines(resouce)
    return True


def random_string(n):
    """ 生成随机字符串 """
    return ''.join(
        random.choice(string.ascii_letters + string.digits) for _ in range(n))


# 生成Secret_Key
print('生成Secret_Key...')
start_timestamp = int(time.time() * 100000)
secret = random_string(32)
print('成功！KEY: %s, 用时: %sms' %
      (secret, str((int(time.time() * 100000) - start_timestamp) / 100)))

# 写.env
print('生成.env文件...')
ENV_CODE = input('请输入环境编号 (1. Production, 2. Development | defualt: 2): ') or 2
ENV = 'Development'
DEBUG = 1
if ENV_CODE == 1:
    ENV = 'Procution'
    DEBUG = 0
if ENV_CODE == 2:
    ENV = 'Development'
    DEBUG = 1

env = [
    'FLASK_APP=run.py\n',
    'FLASK_DEBUG=%s\n' % ENV_CODE,
    'ENV=%s\n' % ENV,
    'SECRET_KEY=%s\n' % secret
]
create_file('.env', env)
print('成功: %s' % ENV)

# 写uwsgi.ini
print('生成uwsgi.ini')

uwsgi = [
    '[uwsgi]\n',
    'module = run:app\n',
    '\n',
    'master = true\n',
    'processes = 5',
    '\n',
    'daemonize = /var/log/uwsgi.%s.log\n' % cur_dir,
    'socket = /tmp/%s.sock\n' % cur_dir,
    'chmod-socket = 660\n',
    'vacuum = true\n',
    '\n',
    'die-on-term = true\n',
    '\n',
    'for-readline = .env\n',
    '  env = %(_)\n',
    'endfor =\n',
]

create_file('uwsgi.ini', uwsgi)
print('成功! socket路径：/tmp/%s.sock' % cur_dir)

# 写service
print('生成%s.service' % cur_dir)

service = [
    '[Unit]\n',
    'Description=uWSGI instance to serve %s\n' % cur_dir,
    'After=network.target\n', '\n', '[Service]\n',
    'User=%s\n' % user, 'Group=www-data\n',
    'WorkingDirectory=/var/www/%s\n' % cur_dir,
    'Environment="PATH=%s/bin"\n' % venv,
    'ExecStart=%s/bin/uwsgi --ini uwsgi.ini\n' % venv, '\n', '[Install]\n',
    'WantedBy=multi-user.target\n'
]

create_file('system/%s.service' % cur_dir, service)
print('成功！service路径：%s/system/%s.service' % (cwd, cur_dir))

# 链接system
is_ln = input('是否需要配置system (1. 需要， 2. 不需要 | 默认：2): ') or 2
print(is_ln)

if is_ln == '1':
    systemd_url = input(
        '请输入您systemd路径 (默认/lib/systemd/system): ') or '/lib/systemd/system'
    status, output = subprocess.Popen('sudo ln -s %s/system/%s.service %s' %
                                      (cwd, cur_dir, systemd_url))
    if status == 0:
        print('成功!')
        print('自行启动命令: sudo systemctl start %s' % cur_dir)
        print('开机启动命令: sudo systemctl enable %s' % cur_dir)
    else:
        print(output)
else:
    print('跳过system的配置')

# Nginx
print('懒了，手动配置nginx的配置吧')