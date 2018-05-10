""" 
这里是打电话的逻辑

1. 验证手机
2. 添加提交diss电话，使用Queue消息队列处理diss
3. 选择call渠道，目前只有bdlxb
"""
import re
import random
import queue
import time
from threading import Thread
from ..call import BDCall

queue = queue.Queue()


def add_queue(phone):
    """ 异步添加队列 """
    thr = Thread(target=producer, args=[phone])
    thr.start()
    return thr


def producer(phone):
    """ 生产者 """
    queue.put(phone)
    consumer()


def consumer():
    """ 消费者 """
    # 是否空闲
    idle = True

    while idle:
        idle = False

        if queue.qsize() > 0:
            # 队列中存在任务
            times = random.randint(1, 10)
            phone = queue.get()

            # call会阻塞，执行完后返回True
            idle = BDCall.add(phone, times)
        else:
            # 队列为空, 消费者空闲，后续等待生产者触发
            print('队列为空，等你来哦')
            idle = True


def check_phone(phone):
    """
    正则匹配电话号码

    :param phone        用户输入的电话号码
    :return phone_num   纯数字的电话号码, phone
    """
    # 去掉非数字的符号
    phone_num = re.sub("\D", "", phone)

    # 座机+手机的正则匹配
    phone_re = re.compile(
        '^0\d{2,3}\d{7,8}$|^1[3456789]\d{9}$|^861[3456789]\d{9}$')

    if phone_re.match(phone_num):
        # 验证通过则返回去除非空字符的纯数字11位座机/手机号码
        if len(phone_num) > 11:
            # 例：+86 180-0000-0000
            return phone_num[-11:-1]
        return phone_num
    else:
        return False