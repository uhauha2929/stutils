
from collections import Counter
from typing import List

from .common import ngrams


def bleu(references: List[List[str]], candidate: List[str], n: int=2) -> float:
    """计算机器翻译的bleu评价指标

    :param references: 参考句子（已分词）集合
    :param candidate: 候选句子（已分词）
    :param n: 连续单词个数(ngram)
    :return: bleu值
    """
    # 统计候选句的ngram个数
    counts = Counter(ngrams(candidate, n)) if len(candidate) >= n else Counter()

    max_counts = {}
    for reference in references:
        # 统计每个参考句的ngram个数
        reference_counts = (
            Counter(ngrams(reference, n)) if len(reference) >= n else Counter()
        )
        # 取候选句和所有参考句的ngram最大的
        for ngram in counts:
            max_counts[ngram] = max(max_counts.get(ngram, 0), reference_counts[ngram])

    # ngram选候选句和参考句最小的个数即同时出现的个数
    clipped_counts = {
        ngram: min(count, max_counts[ngram]) for ngram, count in counts.items()
    }
    print(clipped_counts)
    print(counts)
    numerator = sum(clipped_counts.values())
    denominator = max(1, sum(counts.values()))
    return numerator/denominator
