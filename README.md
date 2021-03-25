### stutils
String, text, file processing, and more.

### Installation
```bash
pip install git+https://github.com/uhauha2929/stutils
```
### Package
```shell
../stutils
│──file
│  │──common.py
│  └──property.py
│──static
│  │──20k.txt.gz
│  └──stopwords.txt.gz
│──string
│  │──anagram.py
│  │──arithmetic.py
│  │──common.py
│  │──conversion.py
│  │──fuzzy.py
│  │──match.py
│  │──metric.py
│  │──palindrome.py
│  │──prefix.py
│  │──segment.py
│  │──suffix.py
│  │──transform.py
│  └──validation.py
│──text
│  │──common.py
│  │──rank.py
│  └──tfidf.py
└──time
   └──common.py
5 directories, 21 files
```
### Uasage
```python
import stutils as st
st.file.print_tree('.')
st.string.rand_string(5)
st.string.match.sunday_search('sadf', 'ad')
st.string.metric.min_edit_dist('asdf', 'fads')
st.string.suffix.SuffixTree('asdf').find('sd')
st.string.segment.Splitter().split('AllthatIneed...')
st.string.fuzzy.BKTree().query('fack')
```
