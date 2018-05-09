""" 修饰器 """
import time
import xml.etree.cElementTree as ET
from functools import wraps
from flask import g, request, make_response
from app import redis_store


# 解析xml消息
def msg_parser(func):
    """ 解析从微信服务器POST而来的XML消息 """
    #
    @wraps(func)
    def wrapper(*args, **kw):

        if request.method == 'POST':
            # 初始化res_msg字典
            g.res_msg = {}

            # 使用ET解析XML
            req_data = ET.fromstring(request.data)

            # 解析的内容放入g.res_msg字典中
            for child in req_data:
                g.res_msg[child.tag] = child.text
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
        if by == 'openid':
            # 根据微信openip区分用户信息
            by = {'openid': lambda: request.values.get('openid')}[by]
        else:
            # 根据ip区分用户信息
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
            g.view_limits = (requests, remaining - 1, time.time() + ttl)

            if remaining > 0:
                # 剩余请求次数>0，则redis记录+1，并进入后续处理
                redis_store.incr(key, 1)
                # 未达到限制次数，记录到g，方便dispatch处理
                g.status_code = 200
                return func(*args, **kw)
            else:
                # return make_response('Too Many Requests', 429)
                # 这里无法直接返回429，而是记录到g.status_code, 方便dispatch处理
                g.status_code = 429
                return func(*args, **kw)

        return wrapped

    return decorator