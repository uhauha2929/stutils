# -*- coding: utf-8 -*-
from math import log
from typing import List, Dict, Tuple
from ..static import load_words_by_freq

whitespace = ' \t\n\r\v\f'
letters = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'
punctuation = r"""!"#$%&'*+,-./:;=?@\^_`|~"""
brackets = r"""()<>[]{}【】"""
all_letters = whitespace + letters + digits + punctuation + brackets


class Splitter(object):

    def __init__(self, word_freq_file: str = None):
        self.words = load_words_by_freq(word_freq_file)
        self.max_word_len = max(map(len, self.words))
        self.loss_dict = self.get_losses(self.words)

    @staticmethod
    def get_losses(words: List[str]) -> Dict[str, float]:
        words.extend(all_letters)
        n = len(words)
        loss_dict = {}
        for rank, word in enumerate(words, start=1):
            loss_dict[word] = log(rank * log(n))
        return loss_dict

    # https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
    def split(self, text: str) -> List[str]:
        """在没有空格的英文句子切分单词"""
        losses = [0]

        def best_match(pos: int) -> Tuple[float, int]:
            # 在当前位置之前最长单词窗口内的损失
            window_losses = enumerate(reversed(losses[max(0, pos - self.max_word_len):pos]))
            # 从当前位置向前查找子串并加上损失，损失最小的子串最可能为单词
            return min((loss + self.loss_dict.get(text[pos - k - 1:pos].lower(), 1e999), k + 1) for k, loss in window_losses)

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
