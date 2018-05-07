""" 使用redis处理聊天时间动作队列 """

from app import redis_store


def set_event(id, event, expire=60 * 60 * 24):
    """ 
    使用redis添加event 
    
    @param  String  :id         唯一字符串，这里使用openID
    @param  String  :event      动作类型，这里默认使用'diss_call'
    @param  String  :expire     过期时间，默认24小时
    @return Boolean :True/False 
    """
    if redis_store.set(id, event):
        # redis设置成功后，设置过期时间
        if redis_store.expire(id, expire):
            # 过期时间设置成功后，返回True
            return True
        else:
            return False
    else:
        return False


def get_event(id):
    """ 
    从redis中获取event

    @param  String  :id         唯一字符，这里使用openID
    @return String  :event      event
    @return None
    """
    event = redis_store.get(id)
    if event:
        # event为bytes，使用decode转为str
        return event.decode('utf-8')
    else:
        return None