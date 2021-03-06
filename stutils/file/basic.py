# -*- coding: utf-8 -*-
# @Author  : uhauha2929
# @Email   : ck143302@gmail.com
import fnmatch
import os
import time
from functools import partial
from itertools import islice
from pathlib import Path
import shutil
from typing import Callable, List, Union
from contextlib import contextmanager

Dir = Union[str, Path]


@contextmanager
def dive_dir(directory: Dir) -> None:
    """方便使用with语句将目录加入当前路径"""
    cwd = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(cwd)


def _match_func(match):
    if match is None:
        return lambda _: True
    return partial(fnmatch.fnmatch, pat=match) \
        if isinstance(match, str) else match


def print_tree(directory: Dir, depth: int = -1,
               only_directories: bool = False,
               limit: int = 1000,
               skip_empty: bool = False,
               pattern: Union[Callable[[str], bool], str] = None) -> None:
    """打印目录树

    :param directory: 目标目录
    :param depth: 目录的深度
    :param only_directories: 是否仅列出文件夹，默认否
    :param limit: 最大文件数量
    :param skip_empty: 是否跳过空目录
    :param pattern: 字符串函数或者通配符匹配文件名，
                    只在only_directories=False时有效
    """
    start = '│──'
    space = '   '
    branch = '│  '
    last = '└──'
    match_func = _match_func(pattern)
    print(directory)
    directory = Path(directory)
    n_directories, n_files = 0, 0

    def _print_tree(path: Path, prefix: str = '', level: int = -1):
        nonlocal n_directories, n_files
        if not level:
            return
        contents = []
        try:
            if only_directories:
                for d in path.iterdir():
                    if d.is_dir():
                        if skip_empty and is_empty_dir(d):
                            continue
                        contents.append(d)
            else:
                for d in path.iterdir():
                    if d.is_file():
                        if match_func(d.name):
                            contents.append(d)
                    else:
                        if skip_empty and is_empty_dir(d):
                            continue
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
            print(f'... length_limit, {limit}, reached, counted:')
        print(f'\n{n_directories} directories'
              + (f', {n_files} files' if n_files else ''))
    except RecursionError:
        print("The directory is too deep to show.")


def join_paths(*paths: Dir) -> str:
    """拼接多个合法路径，返回全路径字符串"""
    path = Path()
    for p in paths:
        path /= p
    return str(path)


def list_files(directory: Dir,
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


def is_empty_dir(directory: Dir) -> bool:
    """判断是否是空目录"""
    return not os.listdir(directory)


def del_empty_dirs(directory: Dir) -> None:
    """批量删除空目录（包括子目录）"""
    n_empty_dirs = 0
    for dir_path, dir_names, _ in os.walk(directory, topdown=False):
        with dive_dir(dir_path):
            for dir_name in dir_names:
                if is_empty_dir(dir_name):
                    os.rmdir(dir_name)
                    n_empty_dirs += 1
                    print('delete directory:', join_paths(dir_path, dir_name))
    print(f'{n_empty_dirs} directories removed.')


def move_merge_dir(src_dir: Dir, dst_dir: Dir) -> None:
    """移动目录到目标目录下，目标目录下如存在同名目录则尝试合并"""
    src_dir, dst_dir = Path(src_dir), Path(dst_dir)
    try:
        shutil.move(str(src_dir), str(dst_dir))
    except shutil.Error:
        for entry in src_dir.iterdir():
            move_merge_dir(entry, join_paths(dst_dir, src_dir.name))
        src_dir.rmdir()


def merge_same_parent(directory: Dir) -> None:
    """合并名称相同且只包含当前目录的父目录"""
    for dir_path, dir_names, files in os.walk(directory, topdown=False):
        if len(dir_names) == 1 and len(files) == 0:
            dir_name = dir_names[0]
            if dir_name == Path(dir_path).name:
                path = join_paths(dir_path, dir_name)
                for entry in Path(path).iterdir():
                    move_merge_dir(entry, dir_path)
                if is_empty_dir(path):
                    os.rmdir(path)


def del_files(directory: Dir,
              pattern: Union[Callable[[str], bool], str] = None) -> None:
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
                print('delete file:', path)
                n_files += 1
    print(f'{n_files} files removed.')


def rename_files(directory: Dir,
                 str_func: Callable[[str], str] = None) -> None:
    """对目录中（包括子目录）的文件进行重命名

    :param directory: 目标目录路径
    :param str_func: 字符串处理函数
    """
    n_renamed_files = 0
    for dir_path, _, files in os.walk(directory):
        with dive_dir(dir_path):
            for file in files:
                os.rename(file, str_func(file))
                print('rename', join_paths(dir_path, file))
                n_renamed_files += 1
    print(f'{n_renamed_files} files renamed.')


def copy_file(src: Dir, dst: Dir) -> None:
    """仅复制文件，不复制权限、元信息"""
    try:
        shutil.copyfile(src, dst)
    except IOError as e:
        print("copy failed! {}".format(e))


def copy_files(src: Dir, dst_dir: Dir, name: str = None) -> None:
    """拷贝文件到指定目录（包括子目录）

    :param src: 源文件路径
    :param dst_dir: 目标目录路径
    :param name: 拷贝后的新文件名，默认和原文件一致
    """
    name = name or os.path.basename(src)
    for dir_path, _, _ in os.walk(dst_dir):
        copy_file(src, os.path.join(dir_path, name))
