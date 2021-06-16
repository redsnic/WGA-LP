# this files contains fuctions useful to simplify some common activities in the creation
# of the blocks of the pipelines

import os
from bisect import bisect_left

def default(dict_, key, default_, index=None):
    """
    Given a dictionary (dict_) and a key (key),
    returns the value of dict_[key] is it exists,
    otherwise returns a default valule (default_)
    :param dict_: a dictionary
    :param key: a key 
    :param default: the default value to be returned in case of failure
    """
    if key in dict_:
        if index == None:
            return dict_[key]
        else:
            return dict_[key][index]
    return default_

def add_tag(tag, filename):
    """
    modifies a filename adding a tag in the extension:
    filename.ext -> filename.tag.ext
    (if the filename has no ".", an extension (.tag) is added)
    :param tag: rag to be added
    :param filename: original filename
    """
    pos = filename.find(".")
    if pos == -1:
        return filename + "." + tag
    return filename[:pos] + "." + tag + filename[pos:]



def get_files_recursively(directory):
    files = []
    for base_path, _, sub_files in os.walk(directory):
        # make relative paths
        if directory.endswith("/"):
            files += [ os.path.join(base_path, x)[len(directory):] for x in sub_files ]
        else:
            files += [ os.path.join(base_path, x)[len(directory)+1:] for x in sub_files ]
    return files


def merge_two_dicts(x, y):
    """Given two dictionaries, merge them into a new dict as a shallow copy."""
    for key, value in y.items():
        x[key] = value
    return x

def binary_search(a, x):
    """
    a: sorted db
    x: element
    """
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    else:
        return None

