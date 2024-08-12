from flask import request, jsonify
from mydb import (query, modify, add)
from utils import encrypt, Examiner

from .public import check_captcha


# 获取数据（登录数据、注册数据）
def get_data(mode: str):
    """
    :param mode:
        mode = 'login'      获取并整理用户发送过来的登录数据
        mode = 'register'   获取并整理用户发送过来的注册数据

    :return:
        如果成功获取数据，则以元组的形式返回整理好的数据
        如果获取数据失败，则返回 int 类型的 1
    """
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    if mode == 'login':
        if not (account and password):
            return 1
        return account, password
    elif mode == 'register':
        repeat = data.get('repeat')
        phone = data.get('phone')
        captcha = data.get('captcha')
        if not (account and password and repeat and phone and captcha):
            return 1
        return account, password, repeat, phone, captcha
    else:
        raise Exception('The mode you selected is incorrect!')


# 检验数据（登录数据、注册数据）
def check_data(mode: str, data):
    """
    :param mode:
        选择 login 模式，则对 login 数据进行验证
        选择 register 模式，则对 register 数据进行验证

    :param data: 要进行验证的数据

    :return:
        如果数据通过验证，则返回 int 类型的 0
        如果数据没有通过验证，则以 json 格式返回"没有通过的原因"的字符信息
    """
    # 实例化一个检查者对象
    e = Examiner()

    # 获取基本数据（login 和 register 都会用到）
    account = data[0]
    password = data[1]

    # 对基本数据进行格式验证
    if not (account.isalpha() and len(account) <= 32):
        return jsonify(msg='账号格式错误！')

    if not e.check_password(password):
        return jsonify(msg='密码格式错误！最少八个字符，至少一个大写字母，一个小写字母和一个数字！')

    # 账号是否存在（login 和 register 都会用到）
    res = query('user', 'account', account)

    # --------------------- 验证登录数据 ---------------------
    if mode == 'login':
        if not res:
            return jsonify(msg='账号或密码错误！')
        if res[4] == '1':
            return jsonify(msg='此账号已注销！')
        if res[5] == '1':
            return jsonify(msg='此账号已被冻结！')
        if not (encrypt(password) == res[2]):
            return jsonify(msg='账号或密码错误！')

        # 通过校验
        return 0

    # --------------------- 验证注册数据 ---------------------
    elif mode == 'register':
        # 其他数据
        repeat = data[2]
        phone = data[3]
        captcha = data[4]

        # 两次输入的密码是否一致（无需操作数据库）
        if password != repeat:
            return jsonify(msg='两次输入的密码不一致！')

        # 手机号格式校验（无需操作数据库）
        if not e.check_phone(phone):
            return jsonify(msg='手机号格式错误！请输入正确的11位手机号！')

        # 账号和手机号是否被占用（操作数据库）
        if res:  # 如果 res 是 None，说明该账号没有被注册
            return jsonify(msg='该账号已被注册！')
        if query('user', 'phone', phone):
            return jsonify(msg='手机号已被占用！')

        # 验证码校验（无需操作数据库）
        if not check_captcha(captcha):
            return jsonify(msg='验证码输入不正确！')

        # 通过校验
        return 0

    # --------------------- 模式是否正确 ---------------------
    else:
        raise Exception('The mode you selected is incorrect!')


# 写入数据（注册数据）
def write_data(data):
    """
    :param data: 要写入数据库的数据
    :return:
        如果写入数据库成功，则返回 int 类型的 0
        如果写入数据库失败，则返回 json 格式的字符信息
    """
    account = data[0]
    password = encrypt(data[1])
    phone = data[3]
    if not add('user', account, password, '0', '0', '0', phone, account):
        return jsonify(msg='注册失败，请重试！')
    return 0


# 注销账号
def cancel(id):
    return modify('user', 'id', id, 'unregistered', '1')
