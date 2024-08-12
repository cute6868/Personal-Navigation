from flask import jsonify, request
from mydb import query, modify, mutil_query


# 创建一个操作者类
class Operator(object):

    def __init__(self, target, value):
        """
        :param target: 要修改数据库的哪一个字段？
        :param value: 要修改为什么值？
        """
        self.__id = None
        self.__target = target
        self.__value = value

    @property
    def goto_prepare(self):
        """
            如果获取不到用户传递过来的账号数据，或者获取的账号数据不在数据库里，则返回 False，表示没有准备好（数据）
            如果获取得到账号数据，且该账号在数据库里，则返回 True，表示准备好了（数据）
        """
        account = request.get_json().get('account')
        if not account:
            return False
        data = query('user', 'account', account)
        if not data:
            return False
        self.__id = data[0]
        return True

    @property
    def goto_execute(self):
        """
        :return:
            执行成功返回 True
            执行失败返回 False
        """
        return modify('user', 'id', self.__id, self.__target, self.__value)


# 设置字段的方法
def set_field(field: str, value: str, message: str):
    """
    :param field: 要修改的字段
    :param value: 修改后的值
    :param message: 操作执行成功后，需要返回的 JSON 字符串留言
    :return: JSON字符串
    """
    obj = Operator(field, value)  # 实例化一个操作者
    res = obj.goto_prepare  # 让操作者去准备
    if res is False:  # 准备失败
        return jsonify(msg='账号输入错误或账号不存在！', code=0)
    # 准备成功
    res = obj.goto_execute  # 让操作者去执行
    if res is False:  # 执行失败
        return jsonify(msg='出错了，请重试！', code=0)
    # 执行成功
    return jsonify(msg=message, code=1)


# 获取用户表数据
def search_data(rows_per_page, which_page):
    """
    :param rows_per_page: 你的每页需要多少行数据
    :param times: 查找第几页
    :return: JSON格式列表数据 or None
    """
    search_target = ['id', 'account', 'identity', 'unregistered', 'frozen', 'phone', 'username', 'email', 'age',
                     'gender', 'introduce']
    data = mutil_query('user', search_target, rows_per_page, which_page)
    if not data:
        return jsonify(msg='查询失败！', data=[], code=0)
    lst = []
    for row in data:
        dic = {
            "id": row[0],
            "account": row[1],
            "identity": row[2],
            "unregistered": row[3],
            "frozen": row[4],
            "phone": row[5],
            "username": row[6],
            "email": row[7],
            "age": row[8],
            "gender": row[9],
            "introduce": row[10]
        }
        lst.append(dic)
    return jsonify(msg='查询成功！', data=lst, code=1)
