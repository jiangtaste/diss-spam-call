import re


def add_queue(phone):
    return True


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