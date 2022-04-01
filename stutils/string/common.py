# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import random
import string
import re
from typing import Callable

special_pw_chars = '^$_@!%*#~?&'


def rand_password(length: int) -> str:
    """6-16位随机密码"""
    if length < 6 or length > 16:
        raise ValueError('Unsupported length: %d' % length)
    password = []
    chars_list = [string.ascii_lowercase, string.ascii_uppercase, string.digits, special_pw_chars]
    remain_length = length
    for i, group in enumerate(chars_list, start=1):
        n = random.randint(1, remain_length - (len(chars_list) - i)) 
        if i == len(chars_list):
            n = remain_length
        password.extend(random.choices(list(group), k=n))
        remain_length -= n
    random.shuffle(password)
    return ''.join(password)


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


def length_of_longest_substring(s: str) -> int:
    """不含有重复字符的最长子串的长度"""
    char_pos = dict()
    max_len = 0
    last_pos = 0
    for i in range(0, len(s)):
        if s[i] in char_pos:
            last_pos = max(char_pos[s[i]],last_pos)
        max_len = max(max_len,i - last_pos + 1)
        char_pos[s[i]] = i + 1
    
    return max_len
