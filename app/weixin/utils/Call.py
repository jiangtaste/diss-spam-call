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
from app import redis_store

queue = queue.Queue()


def add_queue(phone):
    """ 异步添加队列 """
    thr = Thread(target=producer, args=[phone])
    thr.start()
    return thr


def producer(phone):
    """ 生产者 """
    # 随机次数，一切看脸
    times = random.randint(5, 15)
    print('Diss ->' + phone + ': ' + times + 'times!')
    for t in range(1, times):
        queue.put(phone)


class Consumer(Thread):
    """ 消费者类 """

    print('开启消费者')

    def run(self):
        """ 消费者 """
        while True:
            phone = queue.get()
            print(phone)
            if phone:
                BDCall.add(phone)
                print('Done @ {}'.format(time.asctime()))
                print('还剩{}条记录，2分钟后开始处理'.format(queue.qsize()))
                time.sleep(120)
                continue
            print('Null @ {}'.format(time.asctime()))
            time.sleep(120)


c = Consumer()
c.start()


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