""" 微信视图模块 """
import os
import hashlib
import time
from flask import g, request, make_response, render_template
from .decorators import ratelimit, msg_parser
from . import wx
from . import MsgParser
from . import KwParser


@wx.route('/')
@ratelimit(requests=20, window=60, by="ip")
def index():
    """ 无聊的Joke """
    return 'I am Fine, tks for visit.'


@wx.route('/wx', methods=['GET', 'POST'])
@ratelimit(requests=20, window=60, by="openid")
@msg_parser
def weixin():
    """ Wexin """
    if request.method == 'GET':
        # 这里处理微信服务器认证
        if len(request.args) == 0:
            return "Hello, this is the weixin handle view."

        # 获取参数
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')

        # Token, 同公众号服务器配置保持一只
        token = os.getenv('SECRET_KEY')

        # 进行字典排序
        s = [token, timestamp, nonce]
        s.sort()

        # 拼接字符串
        str = ''.join(s)

        # hash
        hasecode = hashlib.sha1(str.encode('utf-8')).hexdigest()
        # 比较
        if hasecode == signature:
            return echostr
        else:
            return "认证失败，不是微信服务器的请求！"

    if request.method == 'POST':
        # 组织回复消息内容
        msg = {
            'to_user_name': g.res_msg['FromUserName'],
            'from_user_name': g.res_msg['ToUserName'],
            'create_time': int(time.time()),
            'content': g.res_msg['Content']
        }

        # response
        reply_xml = render_template('msg.xml', msg=msg)
        response = make_response(reply_xml)
        response.content_type = 'application/xml'

        return response


@wx.after_request
def inject_rate_limit_headers(response):
    """ 将ratelimit信息写入response header """
    try:
        requests, remaining, reset = map(int, g.view_limits)
    except (AttributeError, ValueError):
        return response
    else:
        h = response.headers
        h.add('X-RateLimit-Remaining', remaining)
        h.add('X-RateLimit-Limit', requests)
        h.add('X-RateLimit-Reset', reset)
        return response