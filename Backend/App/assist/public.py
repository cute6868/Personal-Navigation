from flask import session
from mydb import query


# 检查验证码是否匹配
def check_captcha(captcha):
    """
    :param captcha: 要进行校验的验证码
    :return: True or False
    """
    res = session.get('captcha')
    if res is None:
        return False
    if res != captcha:
        session.pop('captcha')  # 检查完毕后，立即清除
        return False
    session.pop('captcha')  # 检查完毕后，立即清除
    return True


# 通过 account 获取对应的 id
def get_id_by_account(account):
    """
    :param account: 要搜索 id 的账号
    :return: None or id
    """
    data = query('user', 'account', account)
    if not data:
        return None
    return data[0]
