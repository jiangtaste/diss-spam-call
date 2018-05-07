""" 消息关键字回复 """
import time
from . import DissCall, EventParser
from . import messages

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
    event = EventParser.get_event(id)

    if event:
        # event存在，优先处理event
        if event == 'diss_call':
            # diss_call骚扰，使用DissCall验证输入的号码
            phone_num = DissCall.check_phone(phone)

            if phone_num:
                # 电话验证通过, 提交骚扰
                if DissCall.start_call(phone_num):
                    # 提交成功

                    msg['Content'] = messages.diss_success.format(phone=phone)
                    return msg
                else:
                    # 提交失败
                    msg['Content'] = messages.diss_failed.format(phone=phone)
                    return msg

            else:
                # 电话验证不通过
                msg['Content'] = messages.invalide_phone
                return msg
        else:
            # 电话验证不通过
            msg['Content'] = messages.unknown_event
            return msg
    elif msg['Content'] in diss_call_keywords:
        # event不存在，但命中diss_call关键字
        # 添加diss_call的event, 默认24小时后过期
        EventParser.set_event(id, 'diss_call')

        # 组织msg
        msg['Content'] = messages.enter_phone
        return msg
    else:
        # 未命中任何关键字
        if msg['MsgType'] == 'text':
            # 仅当文本类型为text时
            msg['Content'] = messages.unknown_command.format(
                command=msg['Content'])
            return msg
        else:
            # 文本类型为event或image等，返回MsgParser处理后的内容
            return msg