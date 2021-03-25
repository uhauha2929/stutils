# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import string
from typing import List, Tuple, Set


def possible_strings(s: str) -> str:
    """通过添加空格形成新的字符串"""
    for i in range(2 ** (len(s) - 1)):
        chars = []
        for j in range(len(s)):
            chars.append(s[j])
            if i & (1 << j):
                chars.append(' ')
        yield ''.join(chars)


def split(word: str) -> List[Tuple[str, str]]:
    """将单词分成两部分，返回所有可能对列表"""
    return [(word[:i], word[i:]) for i in range(len(word) + 1)]


def one_edit_words(word: str) -> Set[str]:
    """返回对某个单词进行一次编辑后的所有单词集合"""
    pairs = split(word)
    alphabet = string.ascii_lowercase
    deletes = [a + b[1:] for (a, b) in pairs if b]
    transposes = [a + b[1] + b[0] + b[2:] for (a, b) in pairs if len(b) > 1]
    replaces = [a + c + b[1:] for (a, b) in pairs for c in alphabet if b]
    inserts = [a + c + b for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)
