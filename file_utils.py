# *- coding:utf-8 -*-

"""
 module for file utils
"""

import os
import shutil

import pandas


def read_file_to_df(file_dir, file_name, ext='.xlsx', sheet_name='Sheet'):
    # type: (object, object, object, object) -> object
    """
    read file from the file_dir, currently we read excel. Once the data type changed, we are convenient to change here.
    :param file_dir:
    :param file_name: file name without extension
    :param ext: file's extension, maybe '.xlsx','.xls' or '.csv'
    :param sheet_name: sheet name
    :return:
    """
    fn_split = file_name.split('.')
    file_name = fn_split[0]  # remove the extension
    if len(fn_split) > 1:
        ext = '.' + fn_split[1]

    # print(file_dir + file_name + ext)
    return pandas.read_excel(file_dir + file_name + ext, sheet_name=sheet_name)



def write_file_without_save(pf, writer, sheet_name='Sheet', index=False):
    pf.to_excel(writer, sheet_name=sheet_name, index=index)


def write_file_with_writer(pf, writer, sheet_name='Sheet', index=False):
    write_file_without_save(pf, writer, sheet_name=sheet_name, index=index)
    writer.save()


def write_file(pf, dst_file_url, dst_file_name, ext='.xlsx', sheet_name='Sheet', index=False):
    fn_split = dst_file_name.split('.')
    dst_file_name = fn_split[0]  # remove the extension
    if len(fn_split) > 1:
        ext = '.' + fn_split[1]
    writer = pandas.ExcelWriter(dst_file_url + dst_file_name + ext)
    write_file_with_writer(pf, writer, sheet_name=sheet_name, index=index)


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
