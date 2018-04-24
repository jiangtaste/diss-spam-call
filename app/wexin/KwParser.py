""" 消息关键字回复 """
from app.models import Query, Action
from . import DissCall

diss_call_keywords = ['骚扰电话', '骚扰号码']


def keywords_parser(msg):
    """
    处理关键字命中规则

    :param msg: 解析后的消息字典（用户）
    :return msg: kw业务处理后的消息字典（返回）
    """
    # 获取数据，方便使用
    phone = msg['Content']
    query_id = msg['FromUserName']

    # 查询query
    print(query_id)
    query = Query.filter_by_id(query_id)
    print(query)

    if query:
        # query存在，优先处理query
        print('query存在: %s: %s' % (query.id, query.action))

        if query.action == 'diss_call':
            # 开始diss_call骚扰，先使用DissCall验证输入的号码
            phone_num = DissCall.check_phone(phone)

            if phone_num:
                # 电话验证通过, 提交骚扰
                if DissCall.start_call(phone_num):
                    # 提交成功
                    msg['Content'] = '成功腹黑骚扰号码%s一次' % phone
                    return msg
                else:
                    # 提交失败
                    msg['Content'] = '腹黑骚扰号码%s失败，请稍后重试！' % phone
                    return msg

            else:
                # 电话验证不通过
                msg['Content'] = '请输入合法的电话号码%s: ' % phone
                return msg
    elif msg['Content'] in diss_call_keywords:
        # query不存在，但命中diss_call关键字
        # 添加diss_call的query, 360s后过期
        action = Action(query_id, 'diss_call', 360)

        # 不在init中触发add，会有诡异问题，单数使用类方法add
        a = Query.save(action)
        print(len(a))
        for i in a:
            print(i.id)
        # print('添加query成功, query_id: %s' % Query.filter_by_id(query_id).id)

        # 组织msg
        msg['Content'] = '请添加骚扰过您的电话（6分钟内有效）'

        return msg
    else:
        # 未命中任何关键字
        msg['Content'] = '不支持命令：%s，若需腹黑骚扰，请先回复“骚扰号码”或“骚扰电话”，然后复制骚扰过你的号码。我们将对其腹黑骚扰...（千万别拿自己的或好友的号码来测试，不对其后果负责）' % msg[
            'Content']

        return msg