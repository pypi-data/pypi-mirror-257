import datetime


def sub_day_stamp(day, fmt='%Y-%m-%d %H:%M:%S'):
    """
    获取以前时间日期
    :param day: 某天前
    :return:
    """
    a = int(datetime.datetime.now().timestamp()) - 60 * 60 * 24 * day
    return datetime.datetime.fromtimestamp(a).strftime(fmt)