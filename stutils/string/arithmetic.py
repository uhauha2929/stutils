# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com


def add_strings(num1: str, num2: str) -> str:
    """给定两个字符串形式的非负整数，返回它们的和"""
    chars = []
    carry, i, j = 0, len(num1) - 1, len(num2) - 1
    while i >= 0 or j >= 0 or carry:
        if i >= 0:
            carry += ord(num1[i]) - ord('0')
            i -= 1
        if j >= 0:
            carry += ord(num2[j]) - ord('0')
            j -= 1
        chars.insert(0, str(int(carry % 10)))
        carry //= 10
    return ''.join(chars)


def multiply_strings(num1: str, num2: str) -> str:
    """给定两个字符串形式的非负整数，返回它们的积"""
    m, n = len(num1), len(num2)
    if m == 0 or n == 0:
        return '0'
    if num1 == '0' or num2 == '0':
        return '0'
    # 乘积的长度最多为m+n
    ans = [0] * (m + n)
    # 从后往前依次和每一位数相乘
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            # 两数第i位和第j位的乘积暂时放到数组的i+j+1位
            ans[i + j + 1] += int(num1[i]) * int(num2[j])
    # 统一处理进位
    for i in range(m + n - 1, 0, -1):
        ans[i - 1] += ans[i] // 10
        ans[i] %= 10
    # ans数组第一位可能位0
    return ''.join(map(str, ans)).lstrip('0')
