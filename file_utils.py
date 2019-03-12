# *- coding:utf-8 -*-

# ------------------------------------
# module for utils
# ------------------------------------

import os
import shutil


# copy file
def copy_file(srcfile, dstfile):
    if not os.path.isfile(srcfile):
        print "%s not exist!" % srcfile
    else:
        fpath, fname = os.path.split(dstfile)  # separate the file path and path name
        if not os.path.exists(fpath):
            os.makedirs(fpath)  # create the destination path
        shutil.copyfile(srcfile, dstfile)  # copy
        print "copy %s -> %s" % (srcfile, dstfile)
