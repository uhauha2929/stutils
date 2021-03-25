# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import math
import warnings
from typing import List, Callable, Dict

from .common import get_tokenized_words


def get_idf(texts: List[List[str]]) -> Dict[str, float]:
    """计算文档的idf值

    :param texts: 文档集合，每篇文档已分好词
    :return: 字典，键为词，值为idf值
    """
    idf = {}
    for words in texts:
        for word in set(words):
            idf[word] = idf.get(word, 0) + 1
    for word in idf:
        idf[word] = math.log(len(texts) / (1 + idf[word]))
    return idf


def get_tfidf(docs: List[str],
              tokenizer: Callable[[str], List[str]] = lambda s: s.split(),
              word_min_len: int = 2,
              stopwords: str = None,
              idf_dict: Dict[str, float] = None) -> List[Dict[str, float]]:
    """返回每个文档中每个词的tfidf值

    :param docs: 文档列表
    :param tokenizer: 文档的分词器，默认空格分割
    :param word_min_len: 关键词的最小长度
    :param stopwords: 停用词路径，默认使用内置停用词
    :param idf_dict: 自定义tfidf权重字典，默认在文档集合中计算
    :return: 字典列表，每个字典代表一篇文档中所有词的tfidf值（未排序）
    """
    if len(docs) == 1 and idf_dict is None:
        warnings.warn("The number of documents is 1, please provide idf dictionary.")
    texts = get_tokenized_words(docs, tokenizer, word_min_len, stopwords)
    idf = idf_dict or get_idf(texts)
    result = []
    for words in texts:
        tfidf = {}
        for word in words:
            tfidf[word] = tfidf.get(word, 0) + 1
        for word in tfidf:
            tfidf[word] = tfidf[word] / len(words) * idf.get(word, 0)
        result.append(tfidf)
    return result
