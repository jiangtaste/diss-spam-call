""" 
使用redis记录事件状态

1. 当聊天内容命中关键字，则记录关键字对应的事件类型
2. 后续聊天内容根据event记录的状态处理业务
3. 因为应用为聊天交互模式，所以同一时刻同一个opened（即用户）只存在一个事件
"""

from app import redis_store


def set_event(id, event, expire=60 * 60 * 24):
    """ 
    使用redis添加event 
    
    @param  id         唯一字符串，这里使用openID
    @param  event      事件类型
    @param  expire     过期时间，默认24小时
    @return key        event的key
    @return None
    """
    key = ":".join(["event", id])

    # 使用set，若已存在key，则自动更新为新的event类型
    if redis_store.set(key, event):
        # redis设置成功后，设置过期时间
        if redis_store.expire(key, expire):
            # 过期时间设置成功后，返回key
            return key
        else:
            return None
    else:
        return None


def get_event(id):
    """ 
    从redis中获取event

    @param  id         唯一字符，这里使用openID
    @return event      event
    @return None
    """
    key = ":".join(["event", id])
    event = redis_store.get(key)
    if event:
        # event为bytes，使用decode转为str
        return event.decode('utf-8')
    else:
        return None