import re

REGEX_EMAIL = "^\\w+([-+.]\\w+)*@\\w+([-.]\\w+)*\\.\\w+([-.]\\w+)*$"
REGEX_MOBILE = "^[1]\\d{10}$"
REGEX_ZH = "^[\\u4e00-\\u9fa5]+$"
REGEX_URL = "[a-zA-z]+://[^\\s]*"
REGEX_IP = "((2[0-4]\\d|25[0-5]|[01]?\\d\\d?)\\.){3}(2[0-4]\\d|25[0-5]|[01]?\\d\\d?)"
REGEX_CHINA_POSTAL_CODE = "[1-9]\\d{5}(?!\\d)"


def is_mobile_simple(phone_number: str) -> bool:
    """
    简单判断是否为手机号
    :param phone_number: 手机号
    :return: 是否为手机号
    """
    return re.match(REGEX_MOBILE, phone_number) is not None


def is_email(email: str) -> bool:
    """
    判断是否为邮箱
    :param email: 邮箱
    :return: 是否为邮箱
    """
    return re.match(REGEX_EMAIL, email) is not None


def is_url(url: str) -> bool:
    """
    判断是否为url
    :param url: url
    :return: 是否为url
    """
    return re.match(REGEX_URL, url) is not None


def is_ip(ip: str) -> bool:
    """
    判断是否为ip
    :param ip: ip
    :return: 是否为ip
    """
    return re.match(REGEX_IP, ip) is not None


def is_zh(zh: str) -> bool:
    """
    判断是否为中文
    :param zh: 字符
    :return: 是否为中文
    """
    return re.match(REGEX_ZH, zh) is not None


def is_chain_postal_code(postal_code: str) -> bool:
    """
    判断是否为中国邮编
    :param postal_code: 邮编
    :return: 是否为中国邮编
    """
    return re.match(REGEX_CHINA_POSTAL_CODE, postal_code) is not None
