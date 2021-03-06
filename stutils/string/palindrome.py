# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com

def is_palindrome(s: str) -> bool:
    """判断是否是回文串"""
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return False
        i += 1
        j -= 1
    return True


def longest_palindrome(text: str, sep: str = '#') -> str:
    """Manacher算法，查找最长回文子串
    时间复杂度：O(n)，空间复杂度：O(n)
    """
    # 预处理
    ext_string = sep.join(sep + text + sep)
    n = len(ext_string)
    p = [0] * n
    center = right_most = 0
    for i in range(1, n - 1):
        # i_mirror表示当前位置的对称点，根据对称性p[i]与p[i_mirror]是可能相等的
        i_mirror = 2 * center - i
        # 如果当前位置i仍然在最右半径左边
        # 那么i的回文半径至少为对称点的值或距边界的距离，两者取最小
        if right_most > i:
            p[i] = min(right_most - i, p[i_mirror])

        # 如果还有超出最右半径的部分则继续从边界处（包含边界）左右拓展
        while ext_string[i + p[i] + 1] == ext_string[i - p[i] - 1]:
            p[i] += 1
        # 如果此时的回文半径大于最右半径，则更新之
        right = i + p[i]
        if right > right_most:
            center = i
            right_most = right

    max_len = center = 0
    for i in range(1, n - 1):
        if p[i] > max_len:
            max_len = p[i]
            center = i
    start = (center - max_len) // 2
    return text[start: start + max_len]
