import re

from constants.database_config import STORE_BATCH_COUNT


def get_insert_columns_and_values(data):
    def get_insert_columns(columns):
        return ','.join(columns)

    def get_insert_values(values):
        """
        根据values获取insert sql
        :param values:
        :return:
        """
        ans = ''
        for value in values:
            if value is None or value == '':
                ans += "'',"
            elif isinstance(value, str):
                # value = value[:20000]
                value = value.replace("'", "")
                value = value.replace("\\", "\\\\")
                ans += ("'{}',".format(value))
            elif isinstance(value, int):
                ans += ("{},".format(value))
            elif isinstance(value, set) or isinstance(value, list):
                tmp = ''
                for v in value:
                    if v and isinstance(v, str):
                        tmp += (',' + v)
                ans += "'{}',".format(tmp[1:])
        return ans[:len(ans) - 1]

    return get_insert_columns(data.keys()), get_insert_values(data.values())


def store_by_batch(name, data_list, conn, store_func):
    """
    批量保存
    :param name: 任务名称
    :param data_list: 保存对象列表
    :param conn: 数据库连接
    :param store_func: 保存方法
    :return:
    """
    if not data_list:
        return
    size = len(data_list)
    i = 0
    cursor = conn.cursor()
    print(store_by_batch.__name__, "执行{}任务开始, 总计{}条待存储数据".format(name, size))
    while i < size:
        endI = min(i + STORE_BATCH_COUNT, size)
        print(store_by_batch.__name__, "startIndex: {}, endIndex: {}".format(i, endI))
        for data in data_list[i: endI]:
            store_func(data, cursor)
        conn.commit()
        i += STORE_BATCH_COUNT
    cursor.close()
    print(store_by_batch.__name__, "执行{}任务结束".format(name))
