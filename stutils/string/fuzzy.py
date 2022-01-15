# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import heapq
import json
import os
from pathlib import Path
from typing import Callable

from .common import case_func_of
from .metric import min_edit_dist
from .transform import one_edit_words
from ..static import load_words_by_freq


class Corrector(object):

    def __init__(self, word_freq_file: str = None):
        self.word_rank = {w: i + 1 for i, w in
                          enumerate(load_words_by_freq(word_freq_file))}

    # 拼写检查器
    def correct(self, word: str, n: int = 5):
        """找出最可能拼错的词，最多两次编辑"""

        def two_edit_words(w):
            return {e2 for e1 in one_edit_words(w) for e2 in one_edit_words(e1)}

        def known(words):
            return {w for w in words if w in self.word_rank}

        case_func = case_func_of(word)
        word = word.lower()
        candidates = (known({word}) or
                      known(one_edit_words(word)) or
                      known(two_edit_words(word)) or
                      [word])

        return list(map(case_func,
                        heapq.nsmallest(n, candidates,
                                        key=self.word_rank.get)))


class BKTree(object):

    def __init__(self,
                 dist_fn: Callable[[str, str], int] = min_edit_dist,
                 save_dir: str = None):
        """Burkhard Keller Tree实现

        用于模糊搜索，单词纠错
        :param dist_fn: 单词距离计算函数，默认最小编辑距离
        :param save_dir: json文件路径
        """
        self.dist_fn = dist_fn
        self.save_dir = save_dir or os.path.expanduser('~')
        self.root = None

    def build(self,
              word_freq_file: str = None,
              save_dir: str = None):
        """自定义构建并保存树

        :param word_freq_file: 词频文件
        :param save_dir: 保存的地址，默认用户目录
        """
        save_dir = save_dir or self.save_dir
        words = load_words_by_freq(word_freq_file)

        def _add(parent, rank, word):
            p_word, _, children = parent
            # 为了满足Json格式，key必须为string
            dist = str(self.dist_fn(p_word, word))
            if dist in children:
                _add(children[dist], rank, word)
            else:
                children[dist] = (word, rank, {})

        self.root = (words.pop(0), 0, {})
        for i, w in enumerate(words):
            _add(self.root, i + 1, w)

        with open(save_dir + '/bk.json', 'wt') as f:
            json.dump(self.root, f)

    def load(self, directory: str = None):
        """加载自定义的json文件"""
        path = Path(directory or self.save_dir) / "bk.json"
        if not path.exists() or path.suffix != '.json':
            raise FileNotFoundError('Tree json file not found.')
        with open(path, 'rt', encoding='utf8') as f:
            self.root = json.load(f)

    def query(self, word, top_n: int = 5, tol: int = 1):
        """查询在容忍度范围内匹配的单词

        :param word: 搜索的单词
        :param top_n: 返回最常用的n个
        :param tol: 容忍的最小距离
        :return: 匹配的单词列表
        """
        if self.root is None:
            raise RuntimeError("Please load or build dictionary first.")

        candidates = []

        def dfs(tree):
            p_word, rank, children = tree
            dist = self.dist_fn(word, p_word)
            if dist <= tol:
                candidates.append((dist, rank, p_word))

            for i in range(dist - tol, dist + tol + 1):
                d = str(i)
                if d in children:
                    dfs(children[d])

        case_fun = case_func_of(word)
        word = word.lower()
        dfs(self.root)
        return [case_fun(word) for _, _, word in heapq.nsmallest(top_n, candidates)]

    def depth(self):
        """返回树的深度"""
        if self.root is None:
            return 0

        def dfs(tree, h):
            _, _, children = tree
            if len(children):
                return max(dfs(child, h + 1) for child in children.values())
            return h

        return dfs(self.root, 0)

    def count(self):
        """返回树的结点数量"""
        if self.root is None:
            return 0

        def dfs(tree, cnt):
            _, _, children = tree
            if len(children):
                return len(children) + sum(dfs(child, cnt) for child in children.values())
            return cnt

        return dfs(self.root, 0)
