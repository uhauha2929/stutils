# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import fnmatch
import os
import time
import warnings
from datetime import datetime
from functools import partial
from itertools import islice
from pathlib import Path
import shutil
from typing import Callable, List, Union
from contextlib import contextmanager
import tempfile

ONE_KB = 1024
ONE_MB = ONE_KB * ONE_KB
ONE_GB = ONE_KB * ONE_MB
ONE_TB = ONE_KB * ONE_GB
ONE_PB = ONE_KB * ONE_TB
ONE_EB = ONE_KB * ONE_PB


def get_temp_dir_path():
    """获取系统的临时目录路径"""
    return tempfile.gettempdir()


def get_user_dir_path():
    """获取用户目录路径"""
    return os.path.expanduser('~')


def get_readable_byte_size(size: int) -> str:
    """以可读方式返回字节大小"""
    if size // ONE_EB:
        info = str(size // ONE_EB) + ' EB'
    elif size // ONE_PB:
        info = str(size // ONE_PB) + ' PB'
    elif size // ONE_TB:
        info = str(size // ONE_TB) + ' TB'
    elif size // ONE_GB:
        info = str(size // ONE_GB) + ' GB'
    elif size // ONE_MB:
        info = str(size // ONE_MB) + ' MB'
    elif size // ONE_KB:
        info = str(size // ONE_KB) + ' KB'
    else:
        info = str(size) + ' bytes'
    return info


@contextmanager
def dive_dir(directory: Union[str, Path]):
    """方便使用with语句将目录加入当前路径"""
    cwd = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cwd)


def mkdir(path: Union[str, Path],
          mode: int = 0o777,
          parents: bool = False,
          exist_ok: bool = False):
    """创建文件夹"""
    Path(path).mkdir(mode=mode, parents=parents, exist_ok=exist_ok)


def set_file_last_modified(file_path: Union[str, Path], dt: datetime):
    """设置文件访问及修改时间"""
    dt_epoch = dt.timestamp()
    os.utime(file_path, (dt_epoch, dt_epoch))


def touch(path: Union[str, Path]):
    """创建文件，如果存在则更新时间"""
    path = Path(path)
    if path.exists():
        set_file_last_modified(path, datetime.now())
    else:
        with open(path, 'w'):
            pass


def size_of(file: Union[str, Path]) -> int:
    """返回文件或者整个目录的大小"""
    file = Path(file)
    if not file.exists():
        raise ValueError(str(file) + ' does not exist.')
    if file.is_file():
        return file.stat().st_size
    else:
        total_size = 0
        with dive_dir(file):
            for f in os.listdir(file):
                total_size += size_of(os.path.abspath(f))
        return total_size


def is_empty_dir(directory: Union[str, Path]) -> bool:
    """判断是否是空目录"""
    return not os.listdir(directory)


def is_symlink(path: Union[str, Path]):
    """判断是否是符号链接"""
    return Path(path).is_symlink()


def _check_file_path(path):
    path = Path(path)
    if path.is_dir():
        raise ValueError(path.name + ' is a directory.')
    if not path.exists():
        raise FileNotFoundError(path.name + ' not found.')


def file2str(path: Union[str, Path],
             encoding: str = 'utf-8') -> str:
    """从文本文件中读取内容为字符串"""
    _check_file_path(path)
    with open(path, 'rt', encoding=encoding) as f:
        return f.read()


def str2file(text: str,
             path: Union[str, Path],
             encoding: str = 'utf-8',
             append: bool = True):
    """将一段文本字符串写入文件"""
    try:
        _check_file_path(path)
    except FileNotFoundError:
        pass  # 如果文件不存在则创建
    with open(path, 'at' if append else 'wt',
              encoding=encoding) as f:
        f.write(text)


def read_lines(path: Union[str, Path],
               encoding: str = 'utf-8',
               line_sep: str = '\n') -> List[str]:
    """从文本文件中读取每一行，并返回列表"""
    return file2str(path, encoding).split(line_sep)


def line_iterator(path: Union[str, Path],
                  encoding: str = 'utf-8'):
    """迭代文件的每一行"""
    _check_file_path(path)
    with open(path, 'rt', encoding=encoding) as f:
        for line in f:
            yield line.strip()


def write_lines(lines: List[str],
                path: Union[str, Path],
                encoding: str = 'utf-8',
                append: bool = True,
                line_sep: str = '\n'):
    """将文本列表写入文件的每一行"""
    try:
        _check_file_path(path)
    except FileNotFoundError:
        pass  # 如果文件不存在则创建
    with open(path, 'at' if append else 'wt',
              encoding=encoding) as f:
        for i, line in enumerate(lines):
            line = line.strip()
            if len(line) == 0:
                warnings.warn(f'Line {i} is empty.')
                continue
            f.write(line + line_sep)


def join_paths(*paths: Union[str, Path]) -> str:
    """拼接多个合法路径，返回全路径字符串"""
    path = Path()
    for p in paths:
        path /= p
    return str(path)


def _match_func(match):
    if match is None:
        return lambda _: True
    return partial(fnmatch.fnmatch, pat=match) \
        if isinstance(match, str) else match


def print_tree(directory: Union[str, Path], depth: int = -1,
               only_directories: bool = False,
               limit: int = 1000,
               skip_empty: bool = False,
               dir_pattern: Union[Callable[[str], bool], str] = None,
               file_pattern: Union[Callable[[str], bool], str] = None):
    """打印目录树

    :param directory: 目标目录
    :param depth: 目录的深度
    :param only_directories: 是否仅列出文件夹，默认否
    :param limit: 最大文件数量
    :param skip_empty: 是否跳过空目录
    :param dir_pattern: 字符串函数或者通配符匹配文件夹
    :param file_pattern: 字符串函数或者通配符匹配文件名，
                    只在only_directories=False时有效
    """
    start = '│──'
    space = '   '
    branch = '│  '
    last = '└──'
    match_file = _match_func(file_pattern)
    match_dir = _match_func(dir_pattern)
    print(directory)
    directory = Path(directory)
    n_directories, n_files = 0, 0

    def _print_tree(path: Path, prefix: str = '', level: int = -1):
        nonlocal n_directories, n_files
        if not level:
            return
        contents = []
        try:
            for d in path.iterdir():
                if d.is_file():
                    if not only_directories and match_file(d.name):
                        contents.append(d)
                else:
                    if skip_empty and is_empty_dir(d):
                        continue
                    if match_dir(d):
                        contents.append(d)
        except PermissionError as e:
            print(e)

        stems = [start] * (len(contents) - 1) + [last]
        for stem, content in zip(stems, contents):
            if content.is_dir():
                yield prefix + stem + content.name
                n_directories += 1
                extension = branch if stem == start else space
                yield from _print_tree(content, prefix + extension, level - 1)
            elif not only_directories:
                yield prefix + stem + content.name
                n_files += 1

    try:
        iterator = _print_tree(directory, level=depth)
        for line in islice(iterator, limit):
            print(line)
        if next(iterator, None):
            print(f'... length_limit, {limit}, reached.')
        print(f'{n_directories} directories'
              + (f', {n_files} files' if n_files else ''))
    except RecursionError:
        print("The directory is too deep to show.")


def file_iterator(path: Union[str, Path]):
    """递归迭代目录中的所有文件"""
    path = Path(path)
    if path.is_file():
        yield path
    else:
        for sub_path in path.iterdir():
            yield from list_files(sub_path)


def list_files(directory: Union[str, Path],
               pattern: Union[Callable[[str], bool], str] = None,
               seconds: int = None,
               include_parent=True) -> List[str]:
    """根据条件列出目录中（包括子目录）的指定文件，默认列出所有文件

    :param directory: 目标目录路径
    :param pattern: 字符串处理函数或者通配符字符串，默认列出所有文件
    :param seconds: 用于返回指定秒数内最近修改的文件
    :param include_parent: 是否包含父目录，默认包含
    :return: 文件名列表
    """
    match_func = _match_func(pattern)
    now = time.time()
    file_list = []
    for dir_path, _, files in os.walk(directory):
        for file in files:
            if match_func(file):
                full_path = join_paths(dir_path, file)
                path = full_path if include_parent else file
                if seconds is None:
                    file_list.append(path)
                else:
                    mtime = os.path.getmtime(full_path)
                    if mtime > (now - seconds):
                        file_list.append(path)
    return file_list


def del_empty_dirs(directory: Union[str, Path],
                   include_self: bool = False):
    """批量删除指定目录下的所有空目录（包括子目录甚至自身）"""
    n_empty_dirs = 0
    for dir_path, dir_names, _ in os.walk(directory, topdown=False):
        with dive_dir(dir_path):
            for dir_name in dir_names:
                if is_empty_dir(dir_name):
                    os.rmdir(dir_name)
                    n_empty_dirs += 1
                    print('Delete directory:',
                          join_paths(dir_path, dir_name))
    if include_self and is_empty_dir(directory):
        os.rmdir(directory)
        n_empty_dirs += 1
        print('Delete directory:', directory)
    print(f'{n_empty_dirs} directories removed.')


def del_files(directory: Union[str, Path],
              pattern: Union[Callable[[str], bool], str] = None):
    """根据条件删除目录中（包括子目录）的指定文件

    :param directory: 目标目录路径
    :param pattern: 字符串处理函数或者通配符字符串，默认删除所有文件
    """
    match_func = _match_func(pattern)
    n_files = 0
    for dir_path, _, files in os.walk(directory, topdown=False):
        for file in files:
            if match_func(file):
                path = join_paths(dir_path, file)
                os.remove(path)
                print('Delete file:', path)
                n_files += 1
    print(f'{n_files} files removed.')


def rename_files(directory: Union[str, Path],
                 str_func: Callable[[str], str] = None):
    """对目录中（包括子目录）的文件进行重命名

    :param directory: 目标目录路径
    :param str_func: 字符串处理函数
    """
    n_renamed_files = 0
    for dir_path, _, files in os.walk(directory):
        with dive_dir(dir_path):
            for file in files:
                os.rename(file, str_func(file))
                print('Rename', join_paths(dir_path, file))
                n_renamed_files += 1
    print(f'{n_renamed_files} files renamed.')


def _check_src_dst_file(src_path, dst_path):
    src_path, dst_path = Path(src_path), Path(dst_path)
    if not src_path.exists():
        raise FileNotFoundError(f'No such file: {src_path}')
    if src_path.is_dir() or dst_path.is_dir():
        raise ValueError('Source or destination must be a file.')


def _check_src_dst_dir(src_path, dst_dir):
    if not src_path.exists():
        raise FileNotFoundError(f'No such file or directory: {src_path}')
    if dst_dir.is_file():
        raise ValueError(f'{dst_dir} is not a directory.')
    if src_path == dst_dir:
        raise ValueError('Cannot move a directory into itself.')
    if src_path.parent == dst_dir:
        raise ValueError(f'{src_path} is already in {dst_dir}.')


def copy_file(src_path: Union[str, Path],
              dst_path: Union[str, Path],
              follow_symlinks: bool = True):
    """复制文件（不复制权限、元信息）并重命名到新的位置（同名则覆盖）"""
    _check_src_dst_file(src_path, dst_path)
    mkdir(dst_path.parent, parents=True, exist_ok=True)
    try:
        shutil.copyfile(src_path, dst_path, follow_symlinks=follow_symlinks)
    except IOError as e:
        print("Copy failed! {}".format(e))


def copy2dir(src_path: Union[str, Path],
             dst_dir: Union[str, Path],
             cover: bool = True,
             follow_symlinks: bool = True):
    """复制文件或目录到目标目录下，目标目录下如存在同名目录则尝试合并

    :param src_path: 目标路径，可以是文件或目录
    :param dst_dir: 移动到的目录，不存在则创建
    :param cover: 若遇到同名文件是选择覆盖还是忽略
    :param follow_symlinks: 是否复制符号链接指向的文件
    """
    src_path, dst_dir = Path(src_path), Path(dst_dir)
    _check_src_dst_dir(src_path, dst_dir)
    try:
        if src_path.is_file():
            dst_path = Path(join_paths(dst_dir, src_path.name))
            if not cover and dst_path.exists():
                return
            copy_file(src_path, dst_path, follow_symlinks)
        else:
            for file in src_path.iterdir():
                copy2dir(file, join_paths(dst_dir, src_path.name),
                         cover, follow_symlinks)
    except shutil.Error as e:
        print(e)


def move_file(src_path: Union[str, Path], dst_path: Union[str, Path]):
    """移动文件并重命名到新的位置（同名则覆盖）"""
    src_path, dst_path = Path(src_path), Path(dst_path)
    _check_src_dst_file(src_path, dst_path)
    mkdir(dst_path.parent, parents=True, exist_ok=True)
    try:
        shutil.move(src_path, dst_path)
    except shutil.Error as e:
        print(e)


def move2dir(src_path: Union[str, Path],
             dst_dir: Union[str, Path],
             cover: bool = True):
    """移动文件或目录到目标目录下，目标目录下如存在同名目录则尝试合并

    :param src_path: 目标路径，可以是文件或目录
    :param dst_dir: 移动到的目录，不存在则创建
    :param cover: 若遇到同名文件是选择覆盖还是忽略
    """
    src_path, dst_dir = Path(src_path), Path(dst_dir)
    _check_src_dst_dir(src_path, dst_dir)
    mkdir(dst_dir, parents=True, exist_ok=True)
    try:
        shutil.move(str(src_path), str(dst_dir))
    except shutil.Error:
        if src_path.is_dir():
            for entry in src_path.iterdir():
                move2dir(entry, join_paths(dst_dir, src_path.name), cover)
            # 目录中所有文件移动完毕，删除该目录
            shutil.rmtree(src_path)
        else:
            # 如果原路径是文件，则判断是否需要覆盖目标文件
            if cover:
                os.remove(join_paths(dst_dir, src_path.name))
                shutil.move(str(src_path), str(dst_dir))


def merge_same_parent(directory: Union[str, Path]):
    """合并名称相同且只包含当前目录的父目录"""
    for dir_path, dir_names, files in os.walk(directory, topdown=False):
        if len(dir_names) == 1 and len(files) == 0:
            dir_name = dir_names[0]
            if dir_name == Path(dir_path).name:
                path = join_paths(dir_path, dir_name)
                for entry in Path(path).iterdir():
                    move2dir(entry, dir_path)
                if is_empty_dir(path):
                    os.rmdir(path)
