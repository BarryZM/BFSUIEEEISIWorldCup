# *- coding:utf-8 -*-

"""
 module for primary analysis before we start data clean
"""

import os

import pandas
from openpyxl.workbook import child as openpyxl_child

import file_utils
from file_directions import origin_file_url, working_file_url, statistic_data_file_url


def data_excel_statistic_info(file_name):
    """
    get the simple statistic info for one data file, the info will be stored under statistic_data_file_url with the
    same file name with file_name, every sheet is one column's info with sheet name be the column's name.
    :param file_name: the file name of the excel, e.g. data.xls
    :return:
    """
    init_file = origin_file_url + file_name
    work_file = working_file_url + file_name

    file_utils.copy_file(init_file, work_file)
    data = pandas.read_excel(init_file)
    writer = pandas.ExcelWriter(unicode(file_utils.check_file_url(statistic_data_file_url) + file_name))
    for column in data.columns:
        described_data = data[column].describe()
        # to name a sheet, there's some rules need to adopt
        m = openpyxl_child.INVALID_TITLE_REGEX.search(column)
        if m:
            for item in m.group():
                scolumn = column.encode('utf-8').replace(item.encode('utf-8'), '-')
                column = scolumn.decode('utf-8')
        described_data.to_excel(writer, sheet_name=column)
    writer.save()


def describe_file_folder(file_holder_url):
    """
    get simple statistic info for all data files in specific file holder
    :param file_holder_url: the folder direction to be described
    :return:
    """
    for file_name in os.listdir(file_holder_url):
        data_excel_statistic_info(file_name)


def describe_work():
    """
    get simple statistic info for all data files in our problem
    :return:
    """
    describe_file_folder(origin_file_url)


def data_categorize():
    """
    categorize these tables
    :return:
    """
    file_name = u'数据初整理.xlsx'
    new_file_name = u'categorize数据初整理.xlsx'
    data = pandas.read_excel(file_name, sheet_name='data')
    categorize_info = pandas.read_excel(file_name, sheet_name='categorize')
    writer = pandas.ExcelWriter(new_file_name)
    for column in categorize_info.columns:
        categorized_data = pandas.DataFrame(columns=data.columns.tolist())
        for row in data.itertuples():
            if categorize_info[column].tolist().__contains__(row[1]):
                row_data = [list(row[1:len(row)])]
                categorized_data = pandas.concat([categorized_data, pandas.DataFrame(row_data, columns=data.columns.tolist())], ignore_index=True)
        categorized_data.to_excel(writer, sheet_name=column)

    writer.save()


print (data_categorize())
