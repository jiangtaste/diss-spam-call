""" 微信msg处理器 """

import time
import xml.etree.cElementTree as ET
from . import freeCall

keywords = ['骚扰号码', '骚扰电话']
action_query = []
xmldict = {}


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

    # 处理业务逻辑

    if len(action_query) > 0:
        # 处理action队列，最后一条任务开始
        action = action_query[-1]

        # 判断action类型
        if action['type'] == 'freeCall':
            phone_num = freeCall.check_phone(Content)
            if phone_num:
                if freeCall.start_call(phone_num):
                    # 移除最后一条任务
                    del action_query[-1]

                    # 返回消息
                    xmldict = {
                        'FromUserName': FromUserName,
                        'ToUserName': ToUserName,
                        'Content': '腹黑骚扰@%s开始...' % Content
                    }
                else:
                    # 返回消息
                    xmldict = {
                        'FromUserName': FromUserName,
                        'ToUserName': ToUserName,
                        'Content': '内部错误，骚扰失败...'
                    }
            else:
                # 返回消息
                xmldict = {
                    'FromUserName': FromUserName,
                    'ToUserName': ToUserName,
                    'Content': '请输入正确的手机号码'
                }
    else:
        # action队列为空，处理新任务
        if Content in keywords:
            # 命中关键字，则添加任务
            xmldict = {
                'FromUserName': FromUserName,
                'ToUserName': ToUserName,
                'Content': '请输入骚扰号码...'
            }
            # 目前只有一个腹黑骚扰工具，所以这里偷懒了
            action_query.append({'type': 'freeCall', 'expire': 72000})
        else:
            # 未命中关键字，什么也不处理
            xmldict = {
                'FromUserName':
                FromUserName,
                'ToUserName':
                ToUserName,
                'Content':
                '不支持此条腹黑命令：%s，若需腹黑骚扰，请先回复“骚扰号码”或“骚扰电话”，然后复制骚扰过你的号码。我们将对其腹黑骚扰...（千万别拿自己的或好友的号码来测试，不对其后果负责）'
                % Content
            }

    return xmldict


def submit_msg(content_dict={': '}, type='text'):
    """
    编制回复信息

    :param content_dict:
    :param type:
    :return:
    """
    to_name = content_dict['FromUserName']
    from_name = content_dict['ToUserName']
    content = content_dict['Content']

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
