# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import heapq
from math import log
from typing import List, Union, Callable, Tuple
from .common import ngrams, get_tokenized_words


def word_rank(doc: Union[List[str], str],
              top_n: int = 10,
              n_iter: int = 10,
              window_size: int = 3,
              alpha: float = 0.85,
              word_min_len: int = 2,
              weight: bool = False,
              tokenizer: Callable[[str], List[str]] = lambda s: s.split(),
              stopwords: str = None) -> List[Union[str, Tuple[str, float]]]:
    """TextRank提取关键词的简单实现

    :param doc: 可以是句子集合或整篇文档
    :param top_n: 选取分数最高的前N个
    :param n_iter: 迭代次数
    :param window_size: 滑动窗口的长度，用于找出共现的词建立边
    :param alpha: 平滑系数
    :param word_min_len: 关键词的最小长度
    :param weight: 是否返回权重
    :param tokenizer: 句子分词器，默认以空格分
    :param stopwords: 自定义停用词文件路径，否则用内置停用词
    :return: 关键词及其分数组成的元组集合
    """
    if isinstance(doc, str):
        doc = [doc]
    texts = get_tokenized_words(doc, tokenizer, word_min_len, stopwords)
    nodes = {}
    for words in texts:
        for ngram in ngrams(words, n=window_size):
            for i in range(len(ngram)):
                links = set()
                for j in range(len(ngram)):
                    if i != j:
                        links.add(ngram[j])
                if ngram[i] not in nodes:
                    nodes[ngram[i]] = set()
                nodes[ngram[i]] |= links
    values = {}
    for _ in range(n_iter):
        for word, links in nodes.items():
            val = 1 - alpha
            for link in links:
                val += alpha * (1 / len(nodes[link])) * values.get(link, 1 / len(nodes))
            values[word] = val

    keywords = [item if weight else item[0] for item in
                heapq.nlargest(top_n, values.items(), key=lambda x: x[1])]
    return keywords


def _similarity_func(s1: Union[str, List[str]],
                     s2: Union[str, List[str]]) -> float:
    m, n = len(s1), len(s2)
    if m == 0 or n == 0 or m == n == 1:
        return 0
    return len(set(s1) & set(s2)) / (log(m) + log(n))


def text_rank(texts: List[str],
              top_n: int = 5,
              n_iter: int = 10,
              alpha: float = 0.85,
              weight: bool = False,
              similarity_func: Callable[[str, str], float] = None,
              tokenizer: Callable[[str], List[str]] = lambda s: s.split(),
              word_min_len: int = 2,
              stopwords: str = None) -> List[Union[str, Tuple[str, float]]]:
    """TextRank提取关键句的简单实现

    :param texts: 句子列表
    :param top_n: 选取前几句
    :param n_iter: 迭代次数
    :param alpha: 平滑系数
    :param weight: 是否返回句子分数
    :param similarity_func: 相似度函数
    :param tokenizer: 分词器
    :param word_min_len: 最短单词长度
    :param stopwords:  停用词文件路径，默认使用内置停用词
    """
    if similarity_func is None:
        similarity_func = _similarity_func
    tokenized_texts = get_tokenized_words(texts, tokenizer, word_min_len, stopwords)
    nodes = {}
    similarities = {}
    for i, words_i in enumerate(tokenized_texts):
        j = i + 1
        while j < len(texts):
            words_j = tokenized_texts[j]
            similarity = similarity_func(words_i, words_j)
            if similarity > 0:
                if i not in nodes:
                    nodes[i] = set()
                if j not in nodes:
                    nodes[j] = set()
                nodes[i].add(j)
                nodes[j].add(i)
                similarities[(i, j)] = similarity
            j += 1

    values = {}
    for _ in range(n_iter):
        for i, links in nodes.items():
            val = 1 - alpha
            for j in links:
                similarity = similarities[(i, j)] if i < j else similarities[(j, i)]
                val += alpha * (similarity / len(nodes[j])) * values.get(j, 1 / len(nodes))
            values[i] = val

    return [(texts[item[0]], item[1]) if weight else texts[item[0]] for item in
            heapq.nlargest(top_n, values.items(), key=lambda x: x[1])]
