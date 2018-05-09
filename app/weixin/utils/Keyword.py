""" 关键字 """

# 硬编码关键字

keywords = [{
    'event': 'diss_call',
    'value': '骚扰号码'
}, {
    'event': 'diss_call',
    'value': '骚扰电话'
}]


def check_keyword(word):
    """
    检查是否命中关键字

    @param  word        需要检测的单词
    @return keyword       若命中，则返回对应的关键字
    @return None        若未命中，则返回None
    """
    for keyword in keywords:
        if word == keyword['value']:
            return keyword
    else:
        return None