""" 这里是打电话的逻 """
import re
import random
import time
from threading import Thread
from ..call import BDCall


def add_queue(phone):
    """ 异步添加队列 """
    thr = Thread(target=BDCall.add, args=[phone])
    thr.start()
    return thr


def get_validated_phone_num(phone):
    """
    获取合法的电话号码，使用正则匹配验证号码

    Args:
        phone:      用户输入的电话号码

    Return:         纯数字的电话号码, 直接用于拨打电话接口，验证不通过则返回为空
    """
    # 去掉非数字的符号
    num = re.sub("\D", "", phone)

    # 座机+手机的正则匹配
    phone_re = re.compile(
        '^0\d{2,3}\d{7,8}$|^1[3456789]\d{9}$|^861[3456789]\d{9}$')

    if phone_re.match(num):
        # 验证通过
        if len(num) > 11:
            # 号码长度大于11，只取后11位
            # 例：+86 180-0000-0000
            phone_num = num[-11:]
        else:
            phone_num = num
    else:
        # 验证不通过，返回None
        phone_num = None

    return phone_num