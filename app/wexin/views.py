""" 微信视图模块 """
from . import wx
from flask import request
import hashlib
import xml.etree.cElementTree as ET
import time
from .templates import reply_msg
""" 下边是路由部分 """


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
        # 处理POST
        xmldata = request.data
        xml_rec = ET.fromstring(xmldata)

        ToUserName = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        MsgType = xml_rec.find('MsgType').text
        Content = xml_rec.find('Content').text
        MsgId = xml_rec.find('MsgId').text

        return reply_msg(msg_type) % (fromUser, ToUserName, int(time.time()),
                                      Content)
