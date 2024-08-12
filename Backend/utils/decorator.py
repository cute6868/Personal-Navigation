from functools import wraps
from flask import session, jsonify
from mydb import query


# 装饰器: 检查登录状态
def check_login_status(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 如果 session 中没有 id，则返回 None
        if not session.get('id'):
            return jsonify(msg='请登录！')
        res = func(*args, **kwargs)
        return res

    return wrapper


# 装饰器: 检查管理员权限
def check_admin_permission(func):
    """
        该装饰器使用前提：当前用户已经登录
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 从数据库中查询数据
        id = session.get('id')
        data = query('user', 'id', id)
        if data[3] != '1':
            return jsonify(msg='权限不足！')
        res = func(*args, **kwargs)
        return res

    return wrapper
