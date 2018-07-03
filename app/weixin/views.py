""" 微信视图模块 """
import os
import hashlib
import time
import json

from flask import g, request, make_response, render_template, jsonify
from app import redis_store, fire_store

from .decorators import ratelimit, msg_parser
from . import wx
from .dispatch import dispatch

# firestore refs
bids_col = fire_store.collection('bids')  # 商户ID

# 批量写入
batch = fire_store.batch()


@wx.route('/')
@ratelimit(requests=20, window=60, by="ip")
def index():
    """ 获取可用商户ID """
    # 从redis中获取bids
    bids = redis_store.get('bids')

    if bids:
        # redis中存在bids
        bids = json.loads(bids)
    else:
        # 不存在，初始化
        bids = list(range(0, 9200))
        redis_store.set('bids', json.dumps(bids))

        # 30天过期
        redis_store.expire('bids', 60 * 60 * 24 * 30)

    return render_template('/index.html', bids=bids)


@wx.route('/sync-bids', methods=['GET', 'POST'])
@ratelimit(requests=20, window=60, by="ip")
def sync_bid():
    """ 同步商户ID """
    if request.method == 'POST':
        # POST
        # 从redis中获取bids
        bids = redis_store.get('bids')

        if bids:
            # redis中存在bids, 解析之
            bids = json.loads(bids)

        # 准备写入事物
        times = len(bids) // 500
        if times > 1:
            # 大于等于500
            for x in range(times):
                # 分片
                for bid in enumerate(bids[(x * 500):(x * 500 + 500)]):
                    batch.set(bids_col.document(str(bid)), {'name': bid})

                # 批量写入fierestore
                batch.commit()

            # 不能被500整除的部分
            for bid in enumerate(bids[(times * 500):]):
                batch.set(bids_col.document(str(bid)), {'name': bid})
        else:
            # 小于500
            for index, bid in enumerate(bids):
                print(index, bid)
                batch.set(bids_col.document(str(index)), {'name': bid})

            # 批量写入fierestore
            batch.commit()

        # 从firestore读取
        bid_docs = bids_col.get()

        bids = []
        for doc in bid_docs:
            bids.append({'id': doc.id, 'data': doc.to_dict()})

        # 生成响应
        response = jsonify(bids)
        response.status_code = 201
        return response
    else:
        # GET
        # 从firestore中获取bids
        bid_docs = bids_col.get()

        bids = []
        for doc in bid_docs:
            bids.append({'id': doc.id, 'data': doc.to_dict()})

        # 生成响应
        response = jsonify(bids)
        response.status_code = 200
        return response


@wx.route('/wx', methods=['GET', 'POST'])
@ratelimit(requests=20, window=60, by="openid")
@msg_parser
def weixin():
    """ Wexin """
    if request.method == 'GET':
        # 这里处理微信服务器认证
        if len(request.args) == 0:
            return "Hello, this is the weixin handle view."

        # 获取参数
        data = request.args
        signature = data.get('signature', '')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr', '')

        # Token, 同公众号服务器配置保持一只
        token = os.getenv('SECRET_KEY')

        # 进行字典排序
        s = [token, timestamp, nonce]
        s.sort()

        # 拼接字符串
        str = ''.join(s)

        # hash
        hasecode = hashlib.sha1(str.encode('utf-8')).hexdigest()
        # 比较
        if hasecode == signature:
            return echostr
        else:
            return "认证失败，不是微信服务器的请求！"

    if request.method == 'POST':
        # 使用dispatch处理消息
        res_msg = dispatch(g.res_msg)
        # 组织回复消息内容
        msg = {
            'to_user_name': res_msg['FromUserName'],
            'from_user_name': res_msg['ToUserName'],
            'create_time': int(time.time()),
            'content': res_msg['Content']
        }

        # response
        res_xml = render_template('msg.xml', msg=msg)
        response = make_response(res_xml)
        response.content_type = 'application/xml'

        return response


@wx.after_request
def inject_rate_limit_headers(response):
    """ 将ratelimit信息写入response header """
    try:
        requests, remaining, reset = map(int, g.view_limits)
    except (AttributeError, ValueError):
        return response
    else:
        h = response.headers
        h.add('X-RateLimit-Remaining', remaining)
        h.add('X-RateLimit-Limit', requests)
        h.add('X-RateLimit-Reset', reset)
        return response