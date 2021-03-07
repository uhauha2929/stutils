包含了字符串、文本处理算法等等······
### 安装
```bash
pip install git+https://github.com/uhauha2929/stutils
```
### 测试
```
>>> import stutils
>>> stutils.file.basic.print_tree('.')
>>> stutils.string.match.z_search('asdfasdf', 'sd')
>>> stutils.string.metric.jaro_winkler_similarity('asdf', 'dfasd')
>>> tree = stutils.string.trie.SuffixTree('eeweewe')
>>> tree.find('wee')
```
