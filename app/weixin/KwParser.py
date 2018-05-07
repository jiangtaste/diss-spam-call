""" 消息关键字回复 """
import time
from . import DissCall, eventParser

diss_call_keywords = ['骚扰电话', '骚扰号码']


def keywords_parser(msg):
    """
    处理关键字命中规则

    :param msg: 解析后的消息字典（用户）
    :return msg: kw业务处理后的消息字典（返回）
    """
    # 获取数据，方便使用
    phone = msg['Content']
    id = msg['FromUserName']

    # 查询event
    event = eventParser.get_event(id)

    if event:
        # event存在，优先处理event
        if event == 'diss_call':
            # diss_call骚扰，使用DissCall验证输入的号码
            phone_num = DissCall.check_phone(phone)

            if phone_num:
                # 电话验证通过, 提交骚扰
                if DissCall.start_call(phone_num):
                    # 提交成功

                    msg['Content'] = '成功DISS{phone}一次，已将其加入DISS骚扰队列。'.format(
                        phone=phone)
                    return msg
                else:
                    # 提交失败
                    msg['Content'] = 'DISS{phone}失败，请稍后重试！'.format(phone=phone)
                    return msg

            else:
                # 电话验证不通过
                msg['Content'] = '请输入合法的电话号码：'
                return msg
        else:
            # 电话验证不通过
            msg['Content'] = '不支持的事件'
            return msg
    elif msg['Content'] in diss_call_keywords:
        # event不存在，但命中diss_call关键字
        # 添加diss_call的event, 默认24小时后过期
        eventParser.set_event(id, 'diss_call')

        # 组织msg
        msg['Content'] = '请添加骚扰过您的电话：'
        return msg
    else:
        # 未命中任何关键字
        if msg['MsgType'] == 'text':
            # 仅当文本类型为text时
            msg['Content'] = '不支持指令：{content}。若需腹黑骚扰，请先回复“骚扰号码”或“骚扰电话”触发骚扰指令，然后输入骚扰过你的号码。（千万别拿自己或好友的号码来测试，不对其后果负责）'.format(
                content=msg['Content'])
            return msg
        else:
            # 文本类型为event或image等，返回MsgParser处理后的内容
            return msg