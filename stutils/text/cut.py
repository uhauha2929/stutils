# -*- coding: utf-8 -*-
__all__ = ['load_words_by_freq', 'cut_into_words']

from math import log
from pathlib import Path
from typing import List, Dict, Tuple
import gzip
import os

MODULE_PATH = os.path.dirname(__file__)

whitespace = ' \t\n\r\v\f'
letters = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
punctuation = r"""!"#$%&'*+,-./:;=?@\^_`|~"""
brackets = r"""()<>[]{}【】"""
all_letters = whitespace + letters + digits + punctuation + brackets


def load_words_by_freq(path: str = None) -> List[str]:
    """从文件加载按频率由大到小排序的单词"""
    if path is None:
        path = Path(MODULE_PATH) / Path('static\\words_by_freq.txt.gz')
    else:
        path = Path(path)
    words = []
    if path.suffix == '.txt':
        f = open(path, 'rt', encoding='utf8')
    else:
        f = gzip.open(path, 'rt', encoding='utf8')
    for line in f:
        line = line.strip()
        if len(line) > 0:
            words.append(line.lower())
    f.close()
    return words


def get_losses(words: List[str]) -> Dict[str, float]:
    words.extend(all_letters)
    n = len(words)
    loss_dict = {}
    for rank, word in enumerate(words, start=1):
        loss_dict[word] = log(rank * log(n))
    return loss_dict


# https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
def cut_into_words(text: str, word_freq_file: str = None) -> List[str]:
    """在没有空格的英文句子切分单词

    >>> cut_into_words('AllthatIneed...')
    ['All', 'that', 'I', 'need', '...']

    :param text: 没有空格的英文文本
    :param word_freq_file: 自定义词频TXT文件路径，每行一个单词，按频率由高到底。
    :return: 切分后的单词列表
    """
    words = load_words_by_freq(word_freq_file)
    max_word_len = max(map(len, words))
    loss_dict = get_losses(words)
    losses = [0]

    def best_match(pos: int) -> Tuple[float, int]:
        # 在当前位置之前最长单词窗口内的损失
        window_losses = enumerate(reversed(losses[max(0, pos - max_word_len):pos]))
        # 从当前位置向前查找子串并加上损失，损失最小的子串最可能为单词
        return min((loss + loss_dict.get(text[pos - k - 1:pos].lower(), 1e999), k + 1) for k, loss in window_losses)

    # 保存最可能单词的长度
    lengths = []
    for i in range(1, len(text) + 1):
        cost, length = best_match(i)
        lengths.append(length)
        losses.append(cost)

    cut_words = []
    i = len(lengths) - 1
    char_set = set(digits + punctuation)
    temp = ''
    while i >= 0:
        length = lengths[i]
        start = i - length + 1
        word = text[start: start + length]
        if word != ' ':
            if word in char_set:
                temp = word + temp
            else:
                if len(temp) > 0:
                    cut_words.insert(0, temp)
                    temp = ''
                cut_words.insert(0, word)
        i -= length
    return cut_words
