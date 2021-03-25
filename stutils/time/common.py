# -*- coding: utf-8 -*-
import calendar
import datetime
import time
from typing import Tuple, Callable


class Timer(object):
    """计时器"""

    def __init__(self, func=time.perf_counter):
        self.elapsed = 0.0
        self._func = func
        self._start = None

    def start(self):
        if self._start is not None:
            raise RuntimeError('Already started')
        self._start = self._func()

    def stop(self):
        if self._start is None:
            raise RuntimeError('Not started')
        end = self._func()
        self.elapsed += end - self._start
        self._start = None

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def countdown(hours: int = 0,
              minutes: int = 0,
              seconds: int = 0,
              func: Callable = None) -> None:
    """ 倒计时

    :param hours: 小时
    :param minutes: 分钟
    :param seconds: 秒
    :param func: 执行结束后调用的函数
    """
    def step():
        nonlocal hours
        nonlocal minutes
        nonlocal seconds
        seconds -= 1
        if seconds == -1:
            seconds = 59
            minutes -= 1
            if minutes == -1:
                minutes = 59
                hours -= 1
                if hours == -1:
                    return False
        return True
    while True:
        time.sleep(1)
        if step():
            print('\r{:0>2d}:{:0>2d}:{:0>2d}'
                  .format(hours, minutes, seconds), end='')
        else:
            print("\rTime's up!")
            break
    if func is not None:
        func()


def timestamp2datetime(timestamp: float,
                       convert_to_local: bool = True,
                       utc: int = 8,
                       is_remove_ms: bool = True) -> datetime:
    """转换UNIX时间戳为datetime对象

    :param timestamp: 时间戳
    :param convert_to_local: 是否转为本地时间
    :param utc: 时区信息，中国为utc+8
    :param is_remove_ms: 是否去除毫秒
    :return: datetime对象
    """
    if is_remove_ms:
        timestamp = int(timestamp)
    dt = datetime.datetime.utcfromtimestamp(timestamp)
    if convert_to_local:
        dt = dt + datetime.timedelta(hours=utc)
    return dt


def convert_date(timestamp: float, pattern: str = '%Y-%m-%d %H:%M:%S') -> str:
    """将时间戳格式化输出"""
    dt = timestamp2datetime(timestamp)
    return dt.strftime(pattern)


_WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
             'Friday', 'Saturday', 'Sunday']


def get_pre_weekday(day_name: str,
                    start_date: datetime = None) -> datetime:
    """获取上一个指定星期名的日期，例如上一个星期五的日期"""
    if start_date is None:
        start_date = datetime.datetime.today()
    day_num = start_date.weekday()
    day_num_target = _WEEKDAYS.index(day_name)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - datetime.timedelta(days=days_ago)
    return target_date


def get_month_range(start_date: datetime = None) -> Tuple:
    """获得某月的起始日期和结束日期

    :param start_date: 可以指定准确的某月的第一天，默认为本月的第一天
    :return: 起始日期和结束日期（下个月的第一天）
    """
    if start_date is None:
        start_date = datetime.date.today().replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + datetime.timedelta(days=days_in_month)
    return start_date, end_date


def date_range(start: datetime, end: datetime,
               step: datetime.timedelta):
    """可以指定起始结束日期和步长的生成器"""
    while start < end:
        yield start
        start += step
