""" 模型 """
import time


class Query(object):
    """ Query 管理类 """

    queries = []

    @staticmethod
    def filter_by_id(id):
        if len(Query.queries) == 0:
            return None

        for query in Query.queries:
            # queries不为空
            if query.id == id:
                # 存在query, 同一用户同一时间只能存在一个query
                if query.expire < int(time.time()):
                    # query已过期，删除此query，返回None
                    Query.queries.remove(query)
                    return None
                else:
                    # query有效，返回query
                    return query
        else:
            return None

    @staticmethod
    def save(query):
        Query.queries.append(query)
        return Query.queries


class Action(object):
    """ Action 类 """

    def __init__(self, id, action, expire):
        """ 初始化 """
        self.id = id
        self.action = action
        self.expire = int(time.time()) + expire  # 过期时间戳: s
