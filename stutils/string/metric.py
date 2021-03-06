# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import math
from typing import Union, List


def min_edit_dist(word1: str, word2: str) -> int:
    """返回最小编辑距离Levenshtein"""
    m = len(word1)
    n = len(word2)
    if m * n == 0:
        return m + n
    # 优化为一维数组（在行上进行滚动），初始化表格第一行
    dp = [i for i in range(n + 1)]
    for i in range(1, m + 1):
        corner = dp[0]  # 表示上一行左边的值，对于新行，就是左上角的值
        dp[0] = i  # dp[0]在表格第一列上遍历
        for j in range(1, n + 1):
            tmp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = corner
            else:
                # dp[j]表示上面的值，dp[j - 1]表示左边的值，corner表示左上角的值
                # 取三者最小的作为新的dp[j]（下一次左边的值）
                dp[j] = min(dp[j] + 1, dp[j - 1] + 1, corner + 1)
            corner = tmp
    return dp[n]


def lcs_length(s1: str, s2: str) -> int:
    """返回最长公共子序列的长度"""
    m = len(s1)
    n = len(s2)
    c = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
            else:
                c[i][j] = c[i][j - 1]
    return c[m][n]


def longest_common_substring(s1: str, s2: str) -> int:
    """返回最长公共子串的长度"""
    m, n = len(s1), len(s2)
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    res = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s2[i - 1] == s1[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > res:
                    res = dp[i][j]
    return res


def jaccard_index(s1: Union[str, list], s2: Union[str, list]) -> float:
    """Jaccard相似度系数"""
    if len(s1) == 0 and len(s2) == 0:
        return 0
    s1, s2 = set(s1), set(s2)
    return len(s1 & s2) / len(s1 | s2)


def sorensen_dice_coef(s1: Union[str, list], s2: Union[str, list]) -> float:
    """Sorensen Dice相似度系数"""
    if len(s1) == 0 and len(s2) == 0:
        return 0
    s1, s2 = set(s1), set(s2)
    return 2 * len(s1 & s2) / (len(s1) + len(s2))


def hamming_dist(s1: Union[str, list], s2: Union[str, list]) -> int:
    """汉明距离"""
    if len(s1) != len(s2):
        raise ValueError('The sequence must be of the same length.')
    return sum(i != j for i, j in zip(s1, s2))


def cosine_similarity(s1: Union[str, list], s2: Union[str, list],
                      unique: bool = True) -> float:
    """计算余弦相似度

    句子要分好词，否则视为字符串，按照字符为单位计算相似度

    :param s1: 字符串或者单词列表
    :param s2: 字符串或者单词列表
    :param unique: 是否只统计元素的存在性
    :return: 相似度
    """
    if len(s1) == 0 or len(s2) == 0:
        return 0
    c1 = {}
    for e in s1:
        c1[e] = c1.get(e, 0) + 1
    c2 = {}
    for e in s2:
        c2[e] = c2.get(e, 0) + 1
    sum1, sum2, dot = 0, 0, 0
    for k in set(c1.keys()) | set(c2.keys()):
        f1, f2 = False, False
        if k in c1:
            sum1 += 1 if unique else c1[k] ** 2
            f1 = True
        if k in c2:
            sum2 += 1 if unique else c2[k] ** 2
            f2 = True
        if f1 and f2:
            dot += 1 if unique else c1[k] * c2[k]
    return dot / (math.sqrt(sum1) * math.sqrt(sum2))


def jaro_winkler_similarity(s1: str, s2: str) -> float:
    """Jaro–Winkler相似度"""

    def get_matched_characters(_s1: str, _s2: str) -> List[str]:
        m, n = len(_s1), len(_s2)
        matched = []
        match_flags = [False] * n  # 排除已经匹配过的
        limit = min(m, n) // 2
        for i in range(m):
            # 计算窗口的边界
            left = max(0, i - limit)
            right = min(i + limit + 1, n)
            for j in range(left, right):
                if not match_flags[j] and _s1[i] == _s2[j]:
                    matched.append(_s1[i])
                    match_flags[j] = True
                    break
        return matched

    # 两个集合应该具有相同的元素且长度相同，字符顺序可能不同，但相同字符应该在同一个窗口内
    matched1 = get_matched_characters(s1, s2)
    matched2 = get_matched_characters(s2, s1)
    match_count = len(matched1)

    # 调换的次数
    tran_count = 0
    for c1, c2 in zip(matched1, matched2):
        if c1 != c2:
            tran_count += 1
    half_tran = tran_count // 2

    if not match_count:
        jaro = 0.0
    else:
        jaro = 1 / 3 * ((match_count / len(s1) +
                         match_count / len(s2) +
                         (match_count - half_tran) / match_count))

    # 共同的前缀最多4个字符
    prefix_len = 0
    for c1, c2 in zip(s1[:4], s2[:4]):
        if c1 != c2:
            break
        prefix_len += 1

    return jaro + 0.1 * prefix_len * (1 - jaro)
