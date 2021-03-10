# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com


def possible_strings(s: str) -> str:
    """通过添加空格形成新的字符串"""
    for i in range(2 ** (len(s) - 1)):
        chars = []
        for j in range(len(s)):
            chars.append(s[j])
            if i & (1 << j):
                chars.append(' ')
        yield ''.join(chars)
