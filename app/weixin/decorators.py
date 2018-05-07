""" 修饰器 """
import xml.etree.cElementTree as ET
from functools import wraps
from time import time
from flask import g, request, make_response
from app import redis_store
from . import messages

# 分发消息：dispatch
# 1. 根据事件类型分发消息
# 2. 根据消息内容分发消息
# 3. 根据错误码分发消息


# 解析xml消息
def msg_parser(func):
    """ 
    解析从微信服务器POST而来的XML消息

    :return :返回一个解析后的消息字典 
    """
    #
    @wraps(func)
    def wrapper(*args, **kw):
        if request.method == 'POST':
            # 使用ET解析XML
            req_data = ET.fromstring(request.data)

            # 获取消息/事件参数, 所有消息均存在To、From、MysType
            ToUserName = req_data.find('ToUserName').text
            FromUserName = req_data.find('FromUserName').text
            MsgType = req_data.find('MsgType').text

            if MsgType == 'text':
                # 文本消息
                Content = req_data.find('Content').text

                g.res_msg = {
                    'ToUserName': ToUserName,
                    'FromUserName': FromUserName,
                    'Content': Content,
                    'MsgType': 'text'
                }
                return func(*args, **kw)
        else:
            # GET
            return func(*args, **kw)

    return wrapper


# http://blog.wongxinjie.com/2016/03/26/简洁Flask-RESTful-API设计/
# 此装饰器版权归上述网址作者所以
# Modified: Paul
def ratelimit(requests=100, window=60, by="ip"):
    """
    接口请求限制

    @param  Num     :request    单位时间内限制总请求次数
    @param  Num     :window     单位时间长度（秒）
    @param  Str     :by         用来区分用户信息的keyID
    """
    if not callable(by):
        # 根据微信openip区分用户信息
        if by == 'openid':
            by = {'openid': lambda: request.values.get('openid')}[by]
        # 根据ip区分用户信息
        elif by == 'ip':
            by = {'ip': lambda: request.remote_addr}[by]

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kw):
            # 存入redis的key
            key = ":".join(["ratelimit", by()])

            # 获取单位时间内剩余的请求次数
            try:
                remaining = requests - int(redis_store.get(key))
            except (ValueError, TypeError):
                remaining = requests
                redis_store.set(key, 0)

            # 获取剩余单位时间周期的时间（秒）
            ttl = redis_store.ttl(key)

            if ttl < 0:
                # 已过期，则设置过期时间（ttl = -2, ttl = -1）
                redis_store.expire(key, window)
                ttl = window

            # 将rate limites情况写入g
            g.view_limits = (requests, remaining - 1, time() + ttl)

            if remaining > 0:
                # 剩余请求次数>0，则redis记录+1，并进入后续处理
                redis_store.incr(key, 1)
                return func(*args, **kw)
            else:
                # return make_response("Too Many Requests", 429)
                # 这里无法直接返回429，而是记录429到g，然后在msg处理逻辑
                g.err_code = 429
                print(g.err_code)
                return func(*args, **kw)

        return wrapped

    return decorator