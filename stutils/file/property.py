# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import re
from typing import Dict, IO, List
import time


class Properties(object):

    """properties配置文件解析工具类

    文件中每一行键值对之间用=或:或空格或tab键分割\n
    在空格和:或=不相邻的情况下，第一次出现的作为分隔符，否则还是以第一次出现的:或=分割\n
    键值对之间的空格被忽略；每一行开头结尾的空格被忽略\n
    以#或!开头的行视为注释，被忽略；空行也被忽略\n
    属性值可以跨多个行，行尾必须是反斜杠，换行后的tab和空格都会忽略\n
    换行符、回车符和制表符可以分别用换行或反斜杠r或tab插入\n
    反斜杠和空格可以用反斜杠来转义，由于空格可以作为分割符，所以属性名中的空格必须要转义
    """
    _chars_map = {i: '\\' + j for i, j in zip(b'\\=: \t\n\r\v\f', '\\=: tnrvf')}
    _map_chars = {j: i for i, j in _chars_map.items()}

    def __init__(self, props: Dict[str, str] = None):
        self.props = props or {}

    @staticmethod
    def sep(text: str) -> List[str]:
        if re.match(r'([^ \t]|(?<=\\) )+[ \t]*(?<!\\)[:=].*', text):
            return re.split(r'(?<!\\)[:=]', text, maxsplit=1)
        return re.split(r'(?<!\\)[ \t]', text, maxsplit=1)

    def _parse(self, lines):
        try:
            it = iter(lines)
            line_no = 0
            for line in it:
                line_no += 1
                if line is None:
                    continue
                line = line.strip()
                if len(line) == 0:
                    continue
                line = line.strip()
                if line[0] == '#' or line[0] == '!':
                    continue
                try:
                    pieces = self.sep(line)
                    if len(pieces) == 1:
                        key, value = pieces[0], ''
                    else:
                        key, value = pieces
                    key = self.unescape(key).strip()
                    value = self.unescape(value).strip()
                    while value.endswith('\\'):
                        value = value[:-1]
                        value += next(it).strip()
                        line_no += 1
                    self._props[key] = value
                except ValueError as e:
                    print('Parsing failed at line:', line_no, e)
        except StopIteration:
            pass

    @classmethod
    def escape(cls, text: str, ignore: str = '') -> str:
        chars_map = cls._chars_map.copy()
        for c in ignore:
            c = ord(c)
            if c in chars_map:
                del chars_map[c]
        return text.translate(chars_map)
    
    @classmethod
    def unescape(cls, text: str) -> str:
        chars = []
        i = 0
        while i < len(text):
            if text[i] == '\\' and i + 1 < len(text):
                chars.append(chr(cls._map_chars[text[i:i + 2]]))
                i += 2
                continue
            chars.append(text[i])
            i += 1
        return ''.join(chars)

    def load(self, stream: IO):
        if stream.mode[0] != 'r':
            raise ValueError('Stream should be opened in read-only mode!')
        try:
            lines = stream.readlines()
            self._parse(lines)
        except IOError as e:
            print(e)

    def get_property(self, key):
        return self._props.get(key, '')

    def set_property(self, key, value):
        self._props[key] = value

    @property
    def props(self):
        return self._props

    @props.setter
    def props(self, props: Dict):
        if not isinstance(props, Dict):
            raise TypeError('Expected a dict')
        self._props = props

    def store(self, out: IO, header=""):
        if out.mode[0] != 'w':
            raise ValueError('Steam should be opened in write mode!')
        try:
            out.write(''.join(('#', header, '\n')))
            local_time = time.strftime('%a %b %d %H:%M:%S %Z %Y', time.localtime())
            out.write(''.join(('#', local_time, '\n')))
            for prop, val in self._props.items():
                out.write(''.join((self.escape(prop), '=',
                                   self.escape(val, ' '), '\n')))
            out.close()
        except IOError as e:
            print(e)

    def __getitem__(self, name):
        return self._props.get(name)

    def __setitem__(self, name, value):
        self._props[name] = value

    def __str__(self):
        return str(self._props)
