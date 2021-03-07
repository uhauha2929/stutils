# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
from collections import OrderedDict
from itertools import islice
from queue import Queue
from typing import List, Dict, Iterable, Union


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

    def list(self):
        """返回所有关键词列表"""
        keywords = []

        def pre_order(current_node, word):
            word.append(current_node.name)
            if current_node.end > 0:
                keywords.append(''.join(word))
            for node in current_node.children.values():
                pre_order(node, word)
            word.pop()

        pre_order(self.root, [])
        return keywords


class AhoCorasick(object):

    class Node(object):

        def __init__(self, name: str):
            self.name = name  # 节点代表的字符
            self.children = OrderedDict()  # 节点的孩子，键为字符，值为节点对象
            self.fail = None  # fail指针，root的指针为None
            self.exist = []  # 如果节点为单词结尾，存放单词的长度

    def __init__(self, keywords: Iterable[str] = None):
        """AC自动机"""
        self.root = self.Node('')
        self.finalized = False
        if keywords is not None:
            for keyword in set(keywords):
                self.add(keyword)

    def add(self, keyword: str):
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
        node = self.root
        for char in keyword:
            if char not in node.children:
                return False
            node = node.children[char]
        return bool(node.exist)

    def list(self):
        """返回所有关键词列表"""
        keywords = []

        def pre_order(current_node, word):
            word.append(current_node.name)
            if current_node.exist:
                keywords.append(''.join(word))
            for node in current_node.children.values():
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


class SuffixTree(object):

    class Node(object):
        def __init__(self, start: int, end: int = -1):
            self.start = start
            self.end = end          # 叶子节点的end默认为-1
            self.suffix_index = -1  # 叶子节点所代表的后缀的起始位置
            self.suffix_link = None
            self.children = OrderedDict()

    def __init__(self, text: str = None, end_tag: str = '$'):
        if len(end_tag) > 1:
            raise ValueError('Invalid special character.')
        self.leaf_end = 0              # 当前遍历字符串的位置，用于动态计算叶节点边的长度
        self.end_tag = end_tag         # 在字符串结尾添加的特殊字符
        self.root = self.Node(-1, -2)  # end设置-2区别于叶子节点end为-1
        self.active_node = self.root
        self.active_edge: int = -1
        self.active_length: int = 0
        self.remainder: int = 0        # 剩余的要添加的后缀的个数
        self.text = None
        if text is not None:
            self.build(text)

    def edge_length(self, node: Node) -> int:
        """动态计算边的长度"""
        edge_end = node.end if node.end != -1 else self.leaf_end
        return edge_end - node.start + 1

    def edge_name(self, node: Node) -> str:
        """返回边代表的子串"""
        edge_end = node.end if node.end != -1 else self.leaf_end
        return self.text[node.start: edge_end + 1]

    def set_suffix_index(self,
                         node: Node = None,
                         height: int = 0):
        """为叶子节点设置代表的后缀的起始位置"""
        node = node or self.root
        for child in node.children.values():
            new_height = height + self.edge_length(child)
            if child.end == -1:
                child.suffix_index = len(self.text) - new_height
            else:
                self.set_suffix_index(child, new_height)

    def get_suffix_index(self, node: Node = None) -> List[int]:
        """返回某个节点下所有叶子节点的后缀的起始位置"""
        node = node or self.root
        positions = []

        def get_suffix_index(cur_node, pos):
            if cur_node.start != -1 and cur_node.end == -1:
                pos.append(cur_node.suffix_index)
            for child in cur_node.children.values():
                get_suffix_index(child, pos)
        get_suffix_index(node, positions)
        return positions

    def build(self, text: str):
        """Ukkonen算法构建后缀树"""
        if self.text is not None:
            raise RuntimeError("The tree has been built.")
        text += self.end_tag
        self.text = text

        for i in range(len(text)):

            self.leaf_end = i
            self.remainder += 1
            # 在所有剩余后缀的构造中记录新创建的内部节点!
            last_new_node = None

            while self.remainder > 0:

                if self.active_length == 0:
                    self.active_edge = i

                if text[self.active_edge] not in self.active_node.children:
                    self.active_node.children[text[self.active_edge]] = self.Node(i)
                    if last_new_node is not None:
                        last_new_node.suffix_link = self.active_node
                        last_new_node = None
                else:
                    # 如果边的长度小于等于需要遍历的长度，则直接跳过边的长度
                    next_node = self.active_node.children[text[self.active_edge]]
                    edge_length = self.edge_length(next_node)
                    if self.active_length >= edge_length:
                        self.active_edge += edge_length
                        self.active_length -= edge_length
                        self.active_node = next_node
                        continue

                    if text[next_node.start + self.active_length] == text[i]:
                        if last_new_node is not None and self.active_node is not self.root:
                            last_new_node.suffix_link = self.active_node
                        self.active_length += 1
                        break

                    split_end = next_node.start + self.active_length - 1
                    split_node = self.Node(next_node.start, split_end)
                    self.active_node.children[text[self.active_edge]] = split_node
                    split_node.children[text[i]] = self.Node(i)
                    next_node.start += self.active_length
                    split_node.children[text[next_node.start]] = next_node

                    if last_new_node is not None:
                        last_new_node.suffix_link = split_node

                    last_new_node = split_node

                self.remainder -= 1
                if self.active_node is self.root and self.active_length > 0:
                    self.active_length -= 1
                    self.active_edge = i - self.remainder + 1
                elif self.active_node is not self.root:
                    self.active_node = self.active_node.suffix_link or self.root

        self.set_suffix_index()

    def print_tree(self, show_id=True, depth: int = -1, limit: int = 100):
        """打印后缀树的树形结构"""
        start = '│──'
        space = '   '
        branch = '│  '
        last = '└──'
        print(f'root|{id(self.root)}' if show_id else 'root')
        current_node = self.root

        def print_tree(node, prefix, level=-1):
            if not level:
                return
            stems = [start] * (len(node.children) - 1) + [last]
            for stem, child in zip(stems, node.children.values()):
                edge_name = self.edge_name(child)
                path = prefix + stem + edge_name
                if show_id:
                    path += '|' + str(id(child))
                    if child.suffix_link is not None:
                        path += '----->' + str(id(child.suffix_link))
                yield path
                if len(child.children) > 0:
                    extension = branch if stem == start else space
                    yield from print_tree(child, prefix + extension, level - 1)

        try:
            it = print_tree(current_node, '', depth)
            for line in islice(it, limit):
                print(line)
            if next(it, None):
                print("Row limit reached.")
        except RecursionError:
            print("The tree is too deep to show.")

    def find(self, sub: str) -> int:
        """查找子串在原字符串中第一次出现的位置

        子串必然是某个后缀的前缀，比起查找，构建树的过程则更耗时
        """
        if len(sub) == 0:
            return 0

        node = self.root
        i = 0  # 指向子串中正在比较的字符位置

        while True:
            if sub[i] not in node.children:
                return -1
            child = node.children[sub[i]]
            edge = self.edge_name(child)
            j = 0
            while i < len(sub) and j < len(edge):
                if sub[i] != edge[j]:
                    break
                i += 1
                j += 1
            if i == len(sub):
                return child.start + j - len(sub)
            elif j == len(edge):
                node = child
            else:
                break
        return -1

    def count_leaves(self, node: Node = None):
        """返回叶子节点个数"""
        node = node or self.root
        n_leaves = 1 if node.end == -1 else 0
        for node in node.children.values():
            n_leaves += self.count_leaves(node)
        return n_leaves

    def _get_matched_node(self, sub: str,
                          start_node: Node = None) -> Union[Node, None]:
        """返回匹配到的最后一条边所在的节点"""
        start_node = start_node or self.root

        def _get_matched_node(s, node):
            if s[0] not in node.children:
                return None
            child = node.children[s[0]]
            edge = self.edge_name(child)
            i = 0
            while i < len(s) and i < len(edge):
                if s[i] != edge[i]:
                    break
                i += 1
            # 如果该边包含该子串，返回该节点下所有的叶子节点的个数
            if i == len(s):
                return child
            # 如果该子串包含该边
            if i == len(edge):
                return _get_matched_node(s[i:], child)
            return None

        return _get_matched_node(sub, start_node)

    def count(self, sub: str) -> int:
        """统计子串出现的次数

        用Text+$构造后缀树，搜索Pattern所在节点下的叶节点数目即为重复次数
        如果Pattern在Text中重复了c次，则Text应有c个后缀以Pattern为前缀
        """
        if len(sub) == 0:
            return 0
        node = self._get_matched_node(sub)
        return 0 if node is None else self.count_leaves(node)

    def find_all(self, sub: str) -> List[int]:
        """找出所有匹配的子串的位置"""
        if len(sub) == 0:
            return []
        node = self._get_matched_node(sub)
        return [] if node is None else self.get_suffix_index(node)

    def longest_repeated_substring(self) -> str:
        """返回任意一个最长的重复子串

        用Text+$构造后缀树，搜索Pattern所在节点下的最深的非叶节点
        从root到该节点所经历过的字符串就是最长重复子串
        """
        def dfs(node, height):
            # 返回最深内部节点至根节点的长度以及该节点的末尾位置
            max_len = height
            max_end = node.end
            for child in node.children.values():
                # 若该节点为内部节点
                if child.end >= 0:
                    h, e = dfs(child, height + self.edge_length(child))
                    if h > max_len:
                        max_len = h
                        max_end = e
            return max_len, max_end

        length, end = dfs(self.root, 0)
        return self.text[end - length + 1: end + 1]

    @classmethod
    def longest_common_substring(cls, s1: str, s2: str,
                                 sep_tag: str = '#',
                                 end_tag: str = '$') -> str:
        """返回两个字符串的任意一个最长公共子串

        连接Text1+#+Text2+$形成新的字符串并构造后缀树
        找到最深的非叶节点，且该节点的叶节点既有#也有$
        """
        raise NotImplementedError

    @classmethod
    def longest_palindrome(cls, s: str,
                           sep_tag: str = '#',
                           end_tag: str = '$') -> str:
        """返回最长回文子串

        将Text整体反转形成新的字符串Text2
        连接 Text+#+Text2+$形成新字符串并构造后缀树
        将问题转变为查找Text和Text1的最长公共部分
        """

        return cls.longest_common_substring(s, s[::-1], sep_tag, end_tag)
