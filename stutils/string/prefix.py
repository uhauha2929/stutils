# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
from typing import List
from .trie import Trie  # 引入前缀树


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
