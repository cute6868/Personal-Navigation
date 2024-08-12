from flask import Blueprint, jsonify, session, send_file, request
import time
from utils.captcha import get_picture
from utils.decorator import check_login_status
from ext import limiter

from ..assist.public import get_id_by_account
from ..assist.assist_base import (get_data, check_data, write_data, cancel)

# 基础部分
# -- 包含功能：
#   1. 验证码
#   2. 登入
#   3. 登出
#   4. 注册
#   5. 注销

# 创建蓝图
bp = Blueprint('base', __name__, url_prefix='/base')


# 验证码
@bp.route('/captcha', methods=['POST'])
@limiter.limit('10/minute', override_defaults=False)
def get_captcha():
    # 生成图片，返回"校验码"和"图片数据流"
    captcha, pic_stream = get_picture()

    # 将"校验码"保存到 这个 ip 用户的 session 中
    session['captcha'] = captcha
    return send_file(pic_stream, mimetype="image/jpeg")


# 登入账号
# 1. 记录每个IP地址的登录次数和最后一次登录时间
ip_login_attempts = {}


# 2. 入口函数
@bp.route('/login', methods=['POST'])
def login():
    # 对已经登录的用户，进行温馨提示
    if session.get('id'):
        return jsonify(msg='你已登录！', code=0)

    # 获取用户的登录数据
    data = get_data('login')
    if data == 1:
        return jsonify(msg='数据不齐全！', code=0)

    # 获取用户的IP地址
    ip_address = request.remote_addr

    # 检查该IP地址是否已经超过五次登录尝试
    if ip_login_attempts.get(ip_address, 0) >= 5:
        last_login_time = ip_login_attempts.get(ip_address + '_time', 0)
        current_time = time.time()
        if current_time - last_login_time < 300:  # 300秒 = 5分钟
            return jsonify(msg='登录次数过多，请稍后再尝试！', code=0)

    # 记录登录次数和登录时间
    ip_login_attempts[ip_address] = ip_login_attempts.get(ip_address, 0) + 1
    ip_login_attempts[ip_address + '_time'] = time.time()

    # 对数据进行校验
    res = check_data('login', data)
    if res != 0:
        return res

    # 登录成功，设置 session，记录用户的编号
    session['id'] = get_id_by_account(data[0])

    # 开启session的有效时间，如果没有配置有效时间，默认一个月时间有效
    session.permanent = True
    return jsonify(msg="登录成功！", code=1)


# 登出账号
@bp.route('/logout', methods=['POST'])
@check_login_status
def logout():
    session['id'] = None
    return jsonify(msg='您已退出登录！', code=1)


# 注册账号
@bp.route('/register', methods=['POST'])
@limiter.limit('6/minute', override_defaults=False)
def register():
    # 获取用户的注册数据
    data = get_data('register')
    if data == 1:
        return jsonify(msg='数据不齐全！', code=0)

    # 对数据进行校验
    res = check_data('register', data)
    if res != 0:
        return res

    # 将数据写入数据库，尝试完成注册
    res = write_data(data)
    if res != 0:
        return res

    # 注册成功
    # 1. 尝试获取用户 id，帮已注册成功的用户进行登录
    id = get_id_by_account(data[0])
    if not id:
        return jsonify(msg='注册成功！请前往登录！', code=1)

    # 2. 成功获取id，进行自动登录操作
    session['id'] = id
    return jsonify(msg='注册成功！', code=1)


# 注销账号
@bp.route('/unregister', methods=['POST'])
@check_login_status
def unregister():
    # 尝试注销账号
    if not cancel(session.get('id')):
        return jsonify(msg='注销失败，请重试！', code=0)

    # 清除 session 退出登录
    session.pop('id')
    return jsonify(msg='注销成功！', code=1)
