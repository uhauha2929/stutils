import gzip
import json
from pathlib import Path
from typing import List, Set
import os

MODULE_DIR = os.path.dirname(__file__)


def load_words_by_freq(path: str = None) -> List[str]:
    """从文件加载按频率由大到小排序的单词"""
    if path is None:
        path = Path(f'{MODULE_DIR}/20k.txt.gz')
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


def load_stopwords(path: str = None) -> Set[str]:
    """从文件中加载停用词，每行一个单词"""
    if path is None:
        path = Path(f'{MODULE_DIR}/stopwords.txt.gz')
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

