from flask import jsonify, session, request
from mydb import query, multi_modify
from utils.myre import Examiner


# 查询登录用户自己的数据
def get_user_data():
    """
    :return: 查询当前登录用户的数据，返回 JSON 字符串
    """
    id = session.get('id')
    data = query('user', 'id', id)
    if data is None:
        return jsonify(msg="查询失败，请重试！", data={}, code=0)
    return jsonify(msg="查询成功！", data={
        "account": data[1],
        "identity": data[3],
        "phone": data[6],
        "username": data[7],
        "email": data[8],
        "age": data[9],
        "gender": data[10],
        "introduce": data[11]
    }, code=1)


# 更新登录用户自己的数据
def update_user_data():
    """
    :return: JSON 字符串
    """
    # 获取数据
    data = request.get_json()

    # 整理数据
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    email = data.get('email')
    age = data.get('age')
    gender = data.get('gender')
    introduce = data.get('introduce')

    # 实例化一个检查者
    obj = Examiner()

    # 如果一个数据都不存在，则提示无法修改
    if not (username or password or phone or email or age or gender or introduce):
        return jsonify(msg='请输入要修改的数据！', code=0)

    # 如果有的数据存在，则对这些数据进行格式检验
    data = {}
    if username:
        if not obj.check_name(username):
            return jsonify(msg='用户名格式错误！只能由中文字符、英文字符、下划线和数字组成，最多32个字符！', code=0)
        data["username"] = username
    if password:
        if not obj.check_password(password):
            return jsonify(msg='密码格式错误！最少八个字符，至少一个大写字母，一个小写字母和一个数字！', code=0)
        data["password"] = password
    if phone:
        if not obj.check_phone(phone):
            return jsonify(msg='手机号格式错误！请输入正确的11位手机号！', code=0)
        data["phone"] = phone
    if email:
        if not obj.check_email(email):
            return jsonify(msg='邮箱格式错误！请输入正确的邮箱！', code=0)
        data["email"] = email
    if age:
        if not (0 < int(age) < 121):
            return jsonify(msg='年龄格式错误！年龄范围是 0 到 121 岁之间！', code=0)
        data["age"] = age
    if gender:
        if not (gender == '0' or gender == '1'):
            return jsonify(msg="性别格式错误！女='0'，男='1'。", code=0)
        data["gender"] = gender
    if introduce:
        if len(introduce) > 64:
            return jsonify(msg='内容不得超过64个字符！', code=0)
        introduce = obj.clean_string(introduce)
        data["introduce"] = introduce

    # 获取用户id
    id = session['id']

    # 更新用户数据
    if multi_modify('user', 'id', id, data):
        return jsonify(msg='修改成功！', code=1)
    return jsonify(msg='修改失败！', code=0)
