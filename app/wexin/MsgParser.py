""" 微信msg处理器 """

import time
import xml.etree.cElementTree as ET


def recv_msg(oriData):
    """ 
    获取从微信服务器POST而来的消息

    :param oriData: post的原data
    :return :返回一个包含发送这、接受者、消息内容的字典 
    """
    xmldata = ET.fromstring(oriData)

    ToUserName = xmldata.find('ToUserName').text
    FromUserName = xmldata.find('FromUserName').text
    MsgType = xmldata.find('MsgType').text
    Content = xmldata.find('Content').text
    MsgId = xmldata.find('MsgId').text

    xmldict = {
        "FromUserName": FromUserName,
        "ToUserName": ToUserName,
        "Content": Content
    }

    return xmldict


def submit_msg(content_dict={"": ""}, type="text"):
    """
    编制回复信息

    :param content_dict:
    :param type:
    :return:
    """
    to_name = content_dict['FromUserName']
    from_name = content_dict['ToUserName']
    content = "对啊, %s, 然后呢？" % content_dict['Content']

    reply_xml = """
    <xml>
        <ToUserName><![CDATA[%s]]></ToUserName>
        <FromUserName><![CDATA[%s]]></FromUserName>
        <CreateTime>%s</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[%s]]></Content>
        <FuncFlag>0</FuncFlag>
    </xml>
    """

    return reply_xml % (to_name, from_name, int(time.time()), content)
