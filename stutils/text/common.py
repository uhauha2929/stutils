# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import warnings
import re
from typing import Union, List, Tuple, Callable
import string

from ..static import load_stopwords


def get_tokenized_words(docs: List[str],
                        tokenizer: Callable[[str], List[str]] = lambda s: s.split(),
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


def ngrams(text: Union[str, List[str]], n: int = 2):
    """返回一个字符串所有的ngrams集合"""
    if n <= 0:
        raise ValueError('Invalid length.')
    if len(text) < n:
        warnings.warn(f'The string length must be greater than {n - 1}.')
        return []
    return [tuple(text[i: i + n]) for i in range(len(text) - 1)]


def bigrams(text: Union[str, List[str]]) -> List[Tuple[str, str]]:
    """返回一个字符串所有bigram集合
    :param text: 分词后的集合，否则以字符为单位
    :return: bigram元组集合
    """
    if len(text) < 2:
        warnings.warn('The string length must be greater than 1.')
        return []
    return [tuple(text[i: i + 2]) for i in range(len(text) - 1)]


def trigrams(text: Union[str, List[str]]) -> List[Tuple[str, str, str]]:
    """返回一个字符串所有trigram集合
    :param text: 分词后的集合，否则以字符为单位
    :return: trigram元组集合
    """
    if len(text) < 3:
        warnings.warn('The string length must be greater than 2.')
        return []
    return [tuple(text[i: i + 3]) for i in range(len(text) - 2)]


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


def remove_extra_spaces(text: str):
    """去除英文句子中多余的空格"""
    n = len(text)
    chars = []
    space_found = False
    for i in range(n):
        if text[i] != ' ':
            if space_found:
                if text[i] not in ',.?':
                    chars.append(' ')
                space_found = False
            chars.append(text[i])
        elif text[i - 1] != ' ':
            space_found = True
    return ''.join(chars)


def remove_punctuation(text: str):
    """去除句子中的标点符号"""
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)
