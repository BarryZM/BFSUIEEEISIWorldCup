# *- coding:utf-8 -*-

"""
 module for file utils
"""

import os
import shutil

import pandas


def read_file(file_dir):
    """
    read file from the file_dir, currently we read excel. Once the data type changed, we are convenient to change here.
    :param file_dir:
    :return:
    """
    return pandas.read_excel(file_dir)


def copy_file(srcfile, dstfile):
    """
    copy file from srcfile to dstfile
    :param srcfile: the file to be copied
    :param dstfile: the file copied to
    :return:
    """
    if not os.path.isfile(srcfile):
        print "%s not exist!" % srcfile
    else:
        fpath, fname = os.path.split(dstfile)  # separate the file path and path name
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # create the destination path
        shutil.copyfile(srcfile, dstfile)  # copy
        print "copy %s -> %s" % (srcfile, dstfile)


def check_file_url(fpath):
    """
    check the file path, if not exists, create the path.
    :param fpath: the path url string
    :return: the origin path string
    """
    if not os.path.exists(fpath):
        os.makedirs(fpath)  # create the destination path
    return fpath
