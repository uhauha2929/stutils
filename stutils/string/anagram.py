# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com


def is_anagram(s1: str, s2: str) -> bool:
    """判断是否两个字符串是同字母异位词"""
    count = {}
    for c in s1:
        count[c] = count.get(c, 0) + 1
    for c in s2:
        if c not in count:
            return False
        count[c] -= 1
    for cnt in count.values():
        if cnt != 0:
            return False
    return True


def remove2anagram(s1: str, s2: str) -> int:
    """返回删除的最小字符数使得两个字符串变成同字母异位词"""
    count = {}
    for c in s1:
        count[c] = count.get(c, 0) + 1
    for c in s2:
        count[c] = count.get(c, 0) - 1
    return sum(map(abs, count.values()))
