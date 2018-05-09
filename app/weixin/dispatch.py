""" 
分发消息至不同处理控制器

1. 根据ratelimit条件，处理429
2. 根据消息类型处理事件：
  1. 文本消息：主要业务类型
       1. 根据关键词分发处理条件，更新event事件
  2. 事件消息：subscribe和unsubscribe事件
  3. 图文消息：image，location，voice，video，等类型消息
4. 根据event状态处理事件 
"""
from flask import make_response, g
from .utils import Keyword, Event, Call
from . import messages


def dispatch(msg):
    """ 
    分发消息
    
    @param msg: msg_parser()解析后的消息
    @return msg: 各路业务处理后返回的消息
    """
    openid = msg['FromUserName']
    msg_type = msg['MsgType']
    if g.status_code == 429:
        # 达到ratelimit限制, 返回消息
        msg['Content'] = messages.out_rate_limit
        return msg
    elif msg_type == 'text':
        # 文本消息
        content = msg['Content']

        # 检测是否命中关键字
        keyword = Keyword.check_keyword(content)

        if keyword:
            # 命中关键字, 根据关键字设置event状态
            Event.set_event(openid, keyword['event'])

            if keyword['event'] == 'diss_call':
                # 当前只有diss_call
                msg['Content'] = messages.enter_phone
                return msg

        # 根据openid查找event
        event = Event.get_event(openid)

        if event:
            # 存在event任务, 处理任务
            if event == 'diss_call':
                # 当前只有diss_call
                phone = Call.check_phone(content)
                if phone == False:
                    msg['Content'] = messages.invalide_phone
                    return msg

                if Call.add_queue(phone):
                    msg['Content'] = messages.diss_success.format(
                        phone=content)
                    return msg
                else:
                    msg['Content'] = messages.diss_failed.format(phone=content)
                    return msg
        else:
            # 未在任务队列中, 返回‘不支持指令’
            msg['Content'] = messages.unknown_command.format(command=content)
            return msg
    elif msg_type == 'event':
        # 事件消息
        if msg['Event'] == 'subscribe':
            # 关注公众号消息, 返回欢迎关注的消息
            msg['Content'] = messages.subscribe
            return msg
        else:
            # 取消关注、上报位置、点击菜单等事件
            # 直接响应空字符，微信不会做任何处理
            return make_response('', 200)
    else:
        # 消息类型为image，location, voice, video, shortvideo, link
        msg['Content'] = messages.unsupported_type
        return msg
