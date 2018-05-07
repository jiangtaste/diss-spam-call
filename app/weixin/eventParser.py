""" 使用redis处理聊天时间动作队列 """

from app import redis_store


def set_event(id, event, expire=60 * 60 * 24):
    """ 
    使用redis添加event 
    
    @param  Str  :id         唯一字符串，这里使用openID
    @param  Str  :event      动作类型，这里默认使用'diss_call'
    @param  Str  :expire     过期时间，默认24小时
    @return Bool :True/False 
    """
    key = ":".join(["event", id])
    if redis_store.set(key, event):
        # redis设置成功后，设置过期时间
        if redis_store.expire(key, expire):
            # 过期时间设置成功后，返回True
            return True
        else:
            return False
    else:
        return False


def get_event(id):
    """ 
    从redis中获取event

    @param  Str  :id         唯一字符，这里使用openID
    @return Str  :event      event
    @return None
    """
    key = key = ":".join(["event", id])
    event = redis_store.get(key)
    if event:
        # event为bytes，使用decode转为str
        return event.decode('utf-8')
    else:
        return None