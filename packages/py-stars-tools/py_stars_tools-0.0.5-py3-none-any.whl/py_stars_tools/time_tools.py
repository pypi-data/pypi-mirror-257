import datetime


def sub_day_stamp(day, fmt='%Y-%m-%d %H:%M:%S'):
    """
    获取以前时间日期
    :param day: 某天前
    :return:
    """
    a = int(datetime.datetime.now().timestamp()) - 60 * 60 * 24 * day
    return datetime.datetime.fromtimestamp(a).strftime(fmt)


def format_time(date: int, fmt='%Y-%m-%d %H:%M:%S'):
    """
    时间格式化
    :param date: 时间戳
    :param fmt: 格式
    :return: 格式化的时间
    """
    if len(str(date)) > 10:
        date = date / 1000
    return datetime.datetime.fromtimestamp(date).strftime(fmt)


def format_date_stamp(date: str, fmt='%Y-%m-%d %H:%M:%S'):
    """
    字符串格式日期转换为时间戳
    :param date: 日期
    :param fmt: 格式
    :return:
    """
    return int(datetime.datetime.strptime(date, fmt).timestamp())

