import hashlib


def md5(data: str):
    """
    获取md5
    :param data: 字符数据
    :return: md5值
    """
    return hashlib.md5(data.encode()).hexdigest()

