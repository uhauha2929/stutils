# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import warnings
import re
from pathlib import Path
from typing import Union, List, Tuple, Set, Callable
import os
import gzip


MODULE_PATH = os.path.dirname(__file__)


def load_stopwords(path: str = None) -> Set[str]:
    """从文件中加载停用词，每行一个单词"""
    if path is None:
        path = Path(MODULE_PATH) / Path('static\\stopwords.txt.gz')
    else:
        path = Path(path)
    stopwords = set()
    if path.suffix == '.txt':
        f = open(path, 'rt', encoding='utf8')
    else:
        f = gzip.open(path, 'rt', encoding='utf8')
    for line in f:
        line = line.strip()
        if len(line) > 0:
            stopwords.add(line.lower())
    f.close()
    return stopwords


def get_tokenized_words(docs: List[str],
                        tokenizer: Callable = lambda s: s.split(),
                        word_min_len: int = 2,
                        stopwords: str = None):
    """文档分词并去除停用词"""
    stopwords = load_stopwords(stopwords)
    texts = []
    for doc in docs:
        words = []
        for word in tokenizer(doc):
            word = word.strip().lower()
            if len(word) >= word_min_len and word not in stopwords:
                words.append(word)
        texts.append(words)
    return texts


def ngrams(string: Union[str, List[str]], n: int = 2):
    """返回一个字符串所有的ngrams集合"""
    if n <= 0:
        raise ValueError('Invalid length.')
    if len(string) < n:
        warnings.warn(f'The string length must be greater than {n - 1}.')
        return []
    return [tuple(string[i: i + n]) for i in range(len(string) - 1)]


def bigrams(string: Union[str, List[str]]) -> List[Tuple[str, str]]:
    """返回一个字符串所有bigram集合
    :param string: 分词后的集合，否则以字符为单位
    :return: bigram元组集合
    """
    if len(string) < 2:
        warnings.warn('The string length must be greater than 1.')
        return []
    return [tuple(string[i: i + 2]) for i in range(len(string) - 1)]


def trigrams(string: Union[str, List[str]]) -> List[Tuple[str, str, str]]:
    """返回一个字符串所有trigram集合
    :param string: 分词后的集合，否则以字符为单位
    :return: trigram元组集合
    """
    if len(string) < 3:
        warnings.warn('The string length must be greater than 2.')
        return []
    return [tuple(string[i: i + 3]) for i in range(len(string) - 2)]


def split_into_sentences(text: str, lang='en') -> List[str]:
    """简单地基于规则对文本进行分句"""
    lang = lang.lower()
    if lang == 'zh':
        text = re.sub(r'([。！!？\\?；;]+)([^”’。！!？\\?])', r"\1\n\2", text)
        text = re.sub(r'(\.{3,6})([^”’])', r"\1\n\2", text)
        text = re.sub(r'(…{1,2})([^”’])', r"\1\n\2", text)
        text = re.sub(r'([。！!？\\?]+[”’])([^，。！!？\\?])', r'\1\n\2', text)
        text = text.rstrip()
        return text.split("\n")
    elif lang == 'en':
        # 由于需要判断常用的缩写和句子的开头，请不要将句子转成小写
        digits = r"(\d)\.(\d)"
        prefix_acronyms = r"(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt|Inc|Ltd|Jr|Sr|Co|etc)[.]"
        acronyms = r"\.([A-Za-z]+)\."
        # 屏蔽数字之间的点和缩写词前后的点
        text = re.sub(digits, "\\1<prd>\\2", text)
        text = re.sub(prefix_acronyms, "\\1<prd>", text)
        text = re.sub(acronyms, "<prd>\\1<prd>", text)
        # 找出句子的末尾并添加<stop>符号作为断句标志
        end = r"([\?\!\.]+\s*[\'\"’”]?)\s*(?=[\"\'“‘]?[A-Z][a-z]*)"
        text = re.sub(end, "\\1<stop>", text)
        # 替换回原来的干扰的点
        text = re.sub('<prd>', '.', text)
        return re.split("<stop>", text)
    else:
        raise ValueError('Unsupported language.')
