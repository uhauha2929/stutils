# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import heapq
from collections import OrderedDict
from typing import List


class Trie(object):

    class Node(object):

        def __init__(self, name: str):
            self.name = name  # 节点代表的字符
            self.children = OrderedDict()  # 节点的孩子，键为字符，值为节点对象
            self.end = 0  # 记录以这个字符结尾的次数

    def __init__(self, keywords: List[str] = None):
        self.root = self.Node('')
        if keywords is not None:
            for keyword in keywords:
                self.add(keyword)

    def add(self, keyword: str):
        """在树中添加关键词"""
        node = self.root
        for char in keyword:
            if char not in node.children:
                node.children[char] = self.Node(char)
            node = node.children[char]
        node.end += 1

    def remove(self, keyword: str) -> bool:
        """删除关键字，返回是否成功"""
        def remove(node, i):
            if i == len(keyword):
                return True
            if keyword[i] in node.children:
                child = node.children[keyword[i]]
                if remove(child, i + 1):
                    if i == len(keyword) - 1:
                        if child.end == 0:
                            return False
                        if child.end >= 1:
                            child.end -= 1
                    del child  # 如果有孩子则不会删除
                    return True
            return False
        return remove(self.root, 0)

    def contains(self, keyword: str) -> bool:
        """是否包含该关键词"""
        node = self.root
        for char in keyword:
            if char not in node.children:
                return False
            node = node.children[char]
        return bool(node.end)

    def count(self, keyword: str) -> int:
        """指定关键词，返回出现的频率"""
        node = self.root
        for char in keyword:
            if char not in node.children:
                return 0
            node = node.children[char]
        return node.end

    def list(self, lexical: bool = False):
        """返回所有关键词列表"""
        keywords = []

        def pre_order(current_node, word):
            word.append(current_node.name)
            if current_node.end > 0:
                keywords.append(''.join(word))
            children = current_node.children.items()
            if lexical:
                children = sorted(children, key=lambda x: x[0])
            for _, node in children:
                pre_order(node, word)
            word.pop()

        pre_order(self.root, [])
        return keywords

    def suggestions(self, key, n: int = 5) -> List[str]:
        """自动补全，根据前缀返回可能的关键词"""
        if n <= 0:
            raise ValueError('The number of suggested words '
                             'must be greater than 0.')
        node = self.root
        not_found = False
        chars = []
        for c in key:
            if c not in node.children:
                not_found = True
                break
            chars.append(c)
            node = node.children[c]

        if not_found:
            return []

        if node.end > 0:
            return [key]

        words = []

        def dfs(_node):
            if _node.end > 0:
                words.append((''.join(chars), _node.end))
            for char, child in _node.children.items():
                chars.append(char)
                dfs(child)
                chars.pop()

        dfs(node)
        words = heapq.nlargest(n, words, key=lambda x: x[1])
        words, _ = zip(*words)
        return list(words)


def common_prefix_length(s1: str, s2: str) -> int:
    """返回两个字符串公共前缀的长度"""
    i = 0
    while i < len(s1) and i < len(s2):
        if s1[i] != s2[i]:
            break
        i += 1
    return i


def longest_common_prefix(strings: List[str]) -> str:
    """返回最长公共前缀"""
    if len(strings) == 0:
        return ""
    prefix = strings[0]
    for i in range(1, len(strings)):
        length = common_prefix_length(strings[i], prefix)
        while length != len(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix
