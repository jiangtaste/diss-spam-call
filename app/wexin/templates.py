""" XML 消息模版 """

text_str = '''
    <xml>
    <ToUserName>![CDATA[%s]]</ToUserName>
    <FromUserName>![CDATA[%s]]</FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType>![CDATA[text]]</MsgType>
    <Content>![CDATA[%s]]</Content>
    </xml>
    '''


def reply_msg(type):
    """ 回复消息 """
    if type == 'text':
        return text_str
