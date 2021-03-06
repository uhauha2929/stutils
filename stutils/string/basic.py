# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import random
import string
from typing import List
import re


def rand_string(length: int) -> str:
    """返回指定长度的随机字符串"""
    return ''.join(random.choices(string.printable, k=length))


def remove_spaces(s: str):
    """去除字符串中的所有空格"""
    return ''.join(re.split('[ \t\n\r\v\f]', s))


def possible_strings(s: str) -> str:
    """通过添加空格形成新的字符串"""
    for i in range(2 ** (len(s) - 1)):
        chars = []
        for j in range(len(s)):
            chars.append(s[j])
            if i & (1 << j):
                chars.append(' ')
        yield ''.join(chars)


def common_prefix_length(s1: str, s2: str) -> int:
    """返回两个字符串公共前缀的长度"""
    i = 0
    while i < len(s1) and i < len(s2):
        if s1[i] != s2[i]:
            break
        i += 1
    return i


def longest_common_prefix(strings: List[str]) -> str:
    """返回最长公共前缀"""
    if len(strings) == 0:
        return ""
    prefix = strings[0]
    for i in range(1, len(strings)):
        length = common_prefix_length(strings[i], prefix)
        while length != len(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix
