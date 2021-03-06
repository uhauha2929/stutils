# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
from typing import List

import unicodedata
import re


def is_pascal_case(s: str) -> bool:
    """是否是大驼峰式命名"""
    return re.match(r'^((?<![A-Z])[A-Z][a-z0-9]*)+$', s) is not None


def is_camel_case(s: str) -> bool:
    """是否是小驼峰式命名"""
    return re.match(r'^[a-z]([a-z0-9]*)((?<![A-Z])[A-Z][a-z0-9]*)*$', s) is not None


def is_snake_case(s: str) -> bool:
    """是否是小蛇式命名"""
    return re.match(r'^[_a-z][a-z0-9_]*$', s) is not None


def is_kebab_case(s: str) -> bool:
    """是否是烤肉串式命名"""
    return re.match(r'^[a-z](-[a-z0-9]+)*$', s) is not None


def camel2words(s: str) -> List[str]:
    """小驼峰式命名转成单词列表"""
    word, words = [], []
    for c in s:
        if c.islower():
            word.append(c)
        else:
            words.append(''.join(word))
            word = [c.lower()]
    words.append(''.join(word))
    return words


def camel2snake(s: str) -> str:
    """小驼峰式转小蛇式命名"""
    return '_'.join(camel2words(s))


def camel2kebab(s: str) -> str:
    """小驼峰式转烤肉串式命名"""
    return '-'.join(camel2words(s))


def snake2words(s: str) -> List[str]:
    """小蛇式转单词列表"""
    return [word.lower() for word in s.split('_') if len(word) > 0]


def snake2camel(s: str) -> str:
    """小蛇式转小驼峰式命名"""
    words = snake2words(s)
    for i in range(1, len(words)):
        words[i] = words[i].capitalize()
    return ''.join(words)


def snake2kebab(s: str) -> str:
    """小蛇式转烤肉串式命名"""
    return '-'.join(snake2words(s))


def kebab2words(s: str) -> List[str]:
    """小蛇式转单词列表"""
    return [word.lower() for word in s.split('-') if len(word) > 0]


def kebab2camel(s: str) -> str:
    """烤肉串式转小驼峰式命名"""
    words = kebab2words(s)
    for i in range(1, len(words)):
        words[i] = words[i].capitalize()
    return ''.join(words)


def kebab2snake(s: str) -> str:
    """烤肉串式转小蛇式命名"""
    return '_'.join(kebab2words(s))


def roman2int(s: str) -> int:
    """罗马数字转换为整数（1~3999）"""
    map2int = {'I': 1, 'V': 5, 'X': 10, 'L': 50,
               'C': 100, 'D': 500, 'M': 1000}
    total = 0
    pre_num = map2int.get(s[0], 0)
    for i in range(1, len(s)):
        num = map2int.get(s[i], 0)
        if pre_num < num:
            total -= pre_num
        else:
            total += pre_num
        pre_num = num
    total += pre_num
    return total


def int2roman(num: int) -> str:
    """整数（1~3999）转换为罗马数字"""
    if not 1 <= num <= 3999:
        raise ValueError('Numbers must be in range of 1-3999.')
    thousands = ["", "M", "MM", "MMM"]
    hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
    return thousands[num // 1000] + hundreds[num % 1000 // 100] + tens[num % 100 // 10] + ones[num % 10]


def strip_accents(s: str) -> str:
    """去除字符上的变音符号，转成相似的英文字符（pýtĥöñ -> python）"""
    return unicodedata.normalize('NFD', s) \
        .encode('ascii', 'ignore').decode('utf-8')
