# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import warnings
from queue import Queue
from typing import List, Iterable, Dict


def brute_search(text: str, pattern: str) -> int:
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


class AhoCorasick(object):
    """AC自动机"""

    class Node(object):

        def __init__(self, name: str):
            self.name = name  # 节点代表的字符
            self.children = {}  # 节点的孩子，键为字符，值为节点对象
            self.fail = None  # fail指针，root的指针为None
            self.exist = []  # 如果节点为单词结尾，存放单词的长度

    def __init__(self, keywords: Iterable[str] = None):
        self.root = self.Node('')
        self.finalized = False
        if keywords is not None:
            for keyword in set(keywords):
                self.add(keyword)

    def add(self, keyword: str):
        """添加关键词"""
        if self.finalized:
            raise RuntimeError('The tree has been finalized!')
        node = self.root
        for char in keyword:
            if char not in node.children:
                node.children[char] = self.Node(char)
            node = node.children[char]
        node.exist.append(len(keyword))

    def remove(self, keyword: str) -> bool:
        """删除关键字，返回是否成功"""
        if self.finalized:
            raise RuntimeError('The tree has been finalized!')

        def remove(node, i):
            if i == len(keyword):
                return True
            if keyword[i] in node.children:
                child = node.children[keyword[i]]
                if remove(child, i + 1):
                    if i == len(keyword) - 1:
                        if not child.exist:
                            return False
                        child.exist.clear()
                    del child  # 如果有孩子，则不会删除
                    return True
            return False

        return remove(self.root, 0)

    def contains(self, keyword: str) -> bool:
        """返回是否包含某个关键词"""
        node = self.root
        for char in keyword:
            if char not in node.children:
                return False
            node = node.children[char]
        return bool(node.exist)

    def list(self, lexical: bool = False):
        """返回所有关键词列表"""
        keywords = []

        def pre_order(current_node, word):
            word.append(current_node.name)
            if current_node.exist:
                keywords.append(''.join(word))
            children = current_node.children.items()
            if lexical:
                children = sorted(children, key=lambda x: x[0])
            for _, node in children:
                pre_order(node, word)
            word.pop()

        pre_order(self.root, [])
        return keywords

    def finalize(self):
        """构建fail指针"""
        queue = Queue()
        queue.put(self.root)
        # 对树进行层次遍历
        while not queue.empty():
            node = queue.get()
            for char in node.children:
                child = node.children[char]
                f_node = node.fail
                # 关键点！需要沿着fail指针向上追溯直至根节点
                while f_node is not None:
                    if char in f_node.children:
                        # 如果该指针指向的节点的孩子中有该字符，则字符节点的fail指针需指向它
                        f_child = f_node.children[char]
                        child.fail = f_child
                        # 同时将长度合并过来，以便最后输出
                        if f_child.exist:
                            child.exist.extend(f_child.exist)
                        break
                    f_node = f_node.fail
                # 如果到根节点也没找到，则将fail指针指向根节点
                if f_node is None:
                    child.fail = self.root
                queue.put(child)
        self.finalized = True

    def search_in(self, text: str) -> Dict[str, List[int]]:
        """在一段文本中查找关键字及其开始位置（可能重复多个）"""
        result = dict()
        if not self.finalized:
            self.finalize()
        node = self.root
        for i, char in enumerate(text):
            matched = True
            # 如果当前节点的孩子中找不到该字符
            while char not in node.children:
                # fail指针为None，说明走到了根节点，找不到匹配的
                if node.fail is None:
                    matched = False
                    break
                # 将fail指针指向的节点作为当前节点
                node = node.fail
            if matched:
                # 找到匹配，将匹配到的孩子节点作为当前节点
                node = node.children[char]
                if node.exist:
                    # 如果该节点存在多个长度，则输出多个关键词
                    for length in node.exist:
                        start = i - length + 1
                        word = text[start: start + length]
                        if word not in result:
                            result[word] = []
                        result[word].append(start)
        return result
