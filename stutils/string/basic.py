# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import random
import string
import re


def rand_string(length: int) -> str:
    """返回指定长度的随机字符串"""
    return ''.join(random.choices(string.printable, k=length))


def remove_spaces(s: str):
    """去除字符串中的所有空格"""
    return ''.join(re.split('[ \t\n\r\v\f]', s))
