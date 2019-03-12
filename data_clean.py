# *- coding:utf-8 -*-

# ------------------------------------
# module for data clean
# ------------------------------------

import xlrd
import xlwt
import pandas
import file_utils
import os
from openpyxl.workbook import child as openpyxl_child

origin_file_url = u'data/赛题1数据材料/赛题1数据集/赛题1数据集/'  # the original file folder url, files in it should be read only
working_file_url = u'data/processed_data/raw_data/'  # the working file folder, a copy from the original file folder, can be changed during work
statistic_data_file_url = u'data/processed_data/statistic_data/'  # statistic info for every table


# get simple statistic info for one data file
def data_excel_statistic_info(file_name):
    init_file = origin_file_url + file_name
    work_file = working_file_url + file_name

    file_utils.copy_file(init_file, work_file)
    data = pandas.read_excel(init_file)
    writer = pandas.ExcelWriter(unicode(file_utils.check_file_url(statistic_data_file_url) + file_name))
    for column in data.columns:
        described_data = data[column].describe()
        m = openpyxl_child.INVALID_TITLE_REGEX.search(column)
        if m:
            for item in m.group():
                scolumn = column.encode('utf-8').replace(item.encode('utf-8'), '-')
                column = scolumn.decode('utf-8')
        described_data.to_excel(writer, sheet_name=column)
    writer.save()


# get simple statistic info for all data files in specific file holder
def describe_file_folder(file_holder_url):
    for file_name in os.listdir(file_holder_url):
        data_excel_statistic_info(file_name)


# get simple statistic info for all data files in our problem
def describe_work():
    describe_file_folder(origin_file_url)
