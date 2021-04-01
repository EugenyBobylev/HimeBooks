"""
Модуль для чтения и записи тегов в файлы (KDE extended attributes)
"""
from typing import Dict

import xattr


def get_meta(file_name) -> Dict:
    """
     Get all extended attributes of file as dictionary
    """
    file_xattr = {}
    attrz = xattr.listxattr(file_name)
    for attrib in attrz:
        value: bytes = xattr.getxattr(file_name, attrib)
        value: str = value.decode(encoding='utf-8')
        file_xattr[attrib] = value
    return file_xattr


def set_meta_tags(file_name: str, tags: str):
    set_xattr(file_name, 'user.xdg.tags', tags)


def get_meta_tags(file_name: str) -> str:
    _meta: Dict = get_meta(file_name)
    key = 'user.xdg.tags'
    if key in _meta:
        tags: bytes = xattr.getxattr(file_name, 'user.xdg.tags')
        tags: str = tags.decode('utf-8')
    else:
        tags: str = ""
    return tags


def set_xattr(file_name: str, attrib_name: str, attrib_value: str):
    xattr.setxattr(file_name, attr=attrib_name, value=bytes(attrib_value, 'utf-8'))


def remove_meta_tags(file_name):
    xattr.removexattr(file_name, 'user.xdg.tags')
