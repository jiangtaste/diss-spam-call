""" 微信视图模块 """
from . import wx
from flask import request, make_response
import hashlib
from . import MsgParser
""" 下边是路由部分 """


@wx.route('/')
def index():
    """ 无聊的Joke """
    return 'I am Fine, tks for visit.'


@wx.route('/wx', methods=['GET', 'POST'])
def weixin():
    """ Wexin """
    if request.method == 'GET':
        if len(request.args) == 0:
            return "Hello, this is the weixin handle view."

        # 获取参数
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')

        # Token, 同公众号服务器配置保持一只
        token = "MII7DnXwxLOrzG0AMVJbhpQjRrECPHcs"

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
        # 处理POST
        xmldict = MsgParser.recv_msg(request.data)
        reply_xml = MsgParser.submit_msg(xmldict)

        # response
        response = make_response(reply_xml)
        response.content_type = 'application/xml'

        return response
