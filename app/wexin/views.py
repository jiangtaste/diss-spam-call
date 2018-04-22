""" 微信视图模块 """
from . import wx
from flask import request
import hashlib


@wx.route('/')
def index():
    """ 无聊的Joke """
    return 'I am Fine, tks for visit.'


@wx.route('/wx', methods=['GET', 'POST'])
def weixin():
    """ Wexin """
    if request.method == 'GET':
        # Token, 同公众号服务器配置保持一只
        token = "MII7DnXwxLOrzG0AMVJbhpQjRrECPHcs"
        # 获取参数
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')

        # 进行字典排序
        s = [token, timestamp, nonce]
        s.sort()

        # 拼接字符串
        str = ''.join(s)

        # 比较
        if hashlib.sha1(str.encode('utf-8')).hexdigest() == signature:
            return echostr
        else:
            return "验证失败"
    if request.method == 'POST':
        request "success"
