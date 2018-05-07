""" 微信msg处理器 """

import time
import xml.etree.cElementTree as ET
from . import messages


def recv_msg(oriData):
    """ 
    获取从微信服务器POST而来的消息

    :param oriData: post的原data
    :return :返回一个包含发送这、接受者、消息内容的字典 
    """
    xmldict = {}

    xmldata = ET.fromstring(oriData)

    # 获取消息/事件参数
    ToUserName = xmldata.find('ToUserName').text
    FromUserName = xmldata.find('FromUserName').text

    MsgType = xmldata.find('MsgType').text

    if MsgType == 'text':
        # 消息类型为文本
        Content = xmldata.find('Content').text
        MsgId = xmldata.find('MsgId').text

        xmldict = {
            'FromUserName': FromUserName,
            'ToUserName': ToUserName,
            'Content': Content,
            'MsgType': MsgType
        }
    elif MsgType in [
            'image', 'voice', 'video', 'shortvideo', 'link', 'location'
    ]:
        # 消息类型为其他类型，暂时统一返回不支持
        xmldict = {
            'FromUserName': FromUserName,
            'ToUserName': ToUserName,
            'Content': messages.unknown_type,
            'MsgType': MsgType
        }
    elif MsgType == 'event':
        # 消息类型为event, 切event为subscribe时
        if xmldata.find('Event').text == 'subscribe':
            xmldict = {
                'FromUserName': FromUserName,
                'ToUserName': ToUserName,
                'Content': messages.subscribe,
                'MsgType': MsgType
            }

    return xmldict