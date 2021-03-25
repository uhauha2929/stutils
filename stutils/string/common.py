# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import random
import string
import re
from typing import Callable


def rand_string(length: int, exclude='') -> str:
    """返回指定长度的随机字符串"""
    chars = string.printable
    if len(exclude) > 0:
        chars = string.printable.translate(str.maketrans('', '', exclude))
    return ''.join(random.choices(chars, k=length))


def remove_spaces(s: str):
    """去除字符串中的所有空格"""
    return ''.join(re.split('[ \t\n\r\v\f]', s))


def case_func_of(word: str) -> Callable[[str], str]:
    """根据单词大小写情况返回相应的转换函数"""
    return (str.upper if word.isupper() else
            str.lower if word.islower() else
            str.title if word.istitle() else
            str)
