import hashlib


def encrypt(data: str):
    """
    -- 对字符串数据进行加密，生成64位十六进制字符串
    :param data: 要进行加密的字符串
    :return: 经过加密后的字符串
    """
    # 密码加盐
    data = 'JaW64f169a7fzaNf' + data + 'c1v98kM0tLV4a8Qe'

    # 使用 SHA-256 算法进行加密
    sha256 = hashlib.sha256()
    sha256.update(str(data).encode('utf-8'))
    return sha256.hexdigest()
