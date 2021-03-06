# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import warnings
from typing import List


def brute_force_search(text: str, pattern: str) -> int:
    """暴力匹配

    时间复杂度：O(m*n)，空间复杂度：O(1)
    """
    warnings.warn('Inefficient method.', DeprecationWarning)
    n, m = len(text), len(pattern)
    if n >= m:
        for k in range(n - m + 1):
            i, j = k, 0
            while i < n and j < m and text[i] == pattern[j]:
                i = i + 1
                j = j + 1
            if j == m:
                return k
    return -1


def kmp_search(text: str, pattern: str) -> int:
    """kmp算法

    时间复杂度：O(m+n)，空间复杂度：O(m)
    """
    warnings.warn('Inefficient method.', DeprecationWarning)
    n = len(text)
    m = len(pattern)
    next_pos = [0] * m
    i, j = 1, 0
    while i < m:
        if pattern[i] == pattern[j]:
            next_pos[i] = j + 1
            j += 1
            i += 1
        elif j != 0:
            j = next_pos[j - 1]
        else:
            next_pos[i] = 0
            i += 1
    i, j = 0, 0
    while i < n and j < m:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        elif j != 0:
            j = next_pos[j - 1]
        else:
            i += 1
    return i - j if j == m else -1


def horspool_search(text: str, pattern: str) -> int:
    """Boyer-Moore-Horspool算法

    时间复杂度：平均O(n)，最坏O(n*m)，最佳O(n/m)，空间复杂度：O(m)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    bad_match_tb = {}
    # 不包含最后一个字符
    for i in range(m - 1):
        bad_match_tb[pattern[i]] = m - i - 1
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j == -1:
            return i
        # 如果该字符在模式串中未出现，返回m
        i += bad_match_tb.get(text[i + m - 1], m)
    return -1


def sunday_search(text: str, pattern: str) -> int:
    """sunday算法

    时间复杂度：平均O(n)，最坏O(n*m)，最佳O(n/m)，空间复杂度：O(m)
    """
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    if m > n:
        return -1
    # 事先计算模式串中每个最靠右的字符移动到末尾的距离
    shift_tb = {}
    for i in range(m):
        shift_tb[pattern[i]] = m - i
    i = 0
    while i <= n - m:
        j = 0
        # 不同于BM算法，这里从前往后匹配
        while text[i + j] == pattern[j]:
            j += 1
            if j >= m:
                return i
        k = i + m  # 当前模式串最后一个字符的下一个位置
        if k >= n:
            return -1
        # 如果k这个位置的字符再模式串中出现，则取事先计算的值，否则移动m+1
        i += shift_tb.get(text[k], m + 1)
    return -1


def z_search(text: str, pattern: str, sep: str = '$') -> List[int]:
    """Z-Algorithm返回所有匹配到的位置，时间复杂度和空间复杂度都为O(n+m)"""
    if len(sep) != 1:
        raise ValueError('Special character length must be 1.')
    n, m = len(text), len(pattern)
    if m == 0:
        return [0]

    def z_array(s):
        # arr[i]表示s[i]之后最大匹配s前缀的长度
        arr = [0] * len(s)
        left = right = 0  # [left, right]目前能够匹配的前缀的最靠右的窗口
        # arr[0]一定为整个字符串的长度，忽略
        for i in range(1, len(s)):
            # 开始生成新的窗口，直接比较
            if i > right:
                left = right = i
                while right < len(s) and s[right - left] == s[right]:
                    right += 1
                arr[i] = right - left
                right -= 1
            else:
                # 向前平移一个窗口
                k = i - left
                # 若当前位置i加上前一个窗口对应位置的前缀长度大于当前窗口的右边界
                # 则说明当前位置代表的前缀长度还可以向右拓展，同时要更新右边界
                if i + arr[k] >= right:
                    left = i
                    while right < len(s) and s[right - left] == s[right]:
                        right += 1
                    arr[i] = right - left
                    right -= 1
                else:
                    # 否则直接利用前一个窗口已经匹配的长度
                    arr[i] = arr[k]
        return arr

    z_arr = z_array(pattern + sep + text)
    return [j - m - 1 for j in range(m, len(z_arr)) if z_arr[j] == m]
