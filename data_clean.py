# *- coding:utf-8 -*-

# ------------------------------------
# module for data clean
# ------------------------------------

import xlrd
import xlwt
import pandas
import file_utils

origin_file_url = u'data/赛题1数据材料/赛题1数据集/赛题1数据集/'
working_file_url = u'data/processed_data/raw_data/'


def data_excel_statistic_info(file_name):
    init_file = origin_file_url + file_name
    work_file = working_file_url + file_name

    file_utils.copy_file(init_file, work_file)
    data = pandas.read_excel(init_file)
    for column in data.columns:
        described_data = data[column].describe()
        print(described_data)
