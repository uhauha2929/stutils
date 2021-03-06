# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import re


def validate_email(s: str) -> bool:
    """校验是否是正确的邮箱格式"""
    return re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+'
                    r'(\.[a-zA-Z0-9-]+)*'
                    r'\.[a-zA-Z0-9]{2,6}$', s) is not None


def validate_url(s: str) -> bool:
    """校验是否是正确的URL格式"""
    return re.match(
        r'^(?:ht|f)tps?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', s, re.IGNORECASE) is not None


def validate_ipv4(ip: str) -> bool:
    """验证是否是合法的ipv4地址"""
    nums = ip.split('.')
    if len(nums) != 3:
        return False
    for x in nums:
        # 块的长度为1-3之间（0~255）
        if len(x) == 0 or len(x) > 3:
            return False
        # 没有额外的前置0，只允许数字，必须小于等于255
        if x[0] == '0' and len(x) != 1 or not x.isdigit() or int(x) > 255:
            return False
    return True


def validate_ipv6(ip: str) -> bool:
    """验证是否是合法的ipv6地址"""
    nums = ip.split(':')
    if len(nums) != 7:
        return False
    hexdigits = '0123456789abcdefABCDEF'
    for x in nums:
        # 每个块至少一个但不超过4个16进制数
        # 只允许16进制的数字： 0-9, a-f, A-F
        if len(x) == 0 or len(x) > 4 or not all(c in hexdigits for c in x):
            return False
    return True


def validate_brackets(text: str) -> bool:
    """判断一个字符串内括号是否成对出现"""
    pairs = {')': '(', ']': '[', '}': '{'}
    stack = list()
    for char in text:
        if char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
        elif char in pairs.values():
            stack.append(char)
    return not stack
