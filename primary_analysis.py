# *- coding:utf-8 -*-

"""
 module for primary analysis before we start data clean
"""
import os
import sys

import numpy
import pandas
import xlrd
import xlsxwriter as xlsxwt
from openpyxl.workbook import child as openpyxl_child

import file_utils
from file_directions import origin_file_url, working_file_url, statistic_data_file_url, categorized_data_file_url

reload(sys)
sys.setdefaultencoding('utf-8')


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
                categorized_data = pandas.concat(
                    [categorized_data, pandas.DataFrame(row_data, columns=data.columns.tolist())], ignore_index=True)
        categorized_data.to_excel(writer, sheet_name=column)

    writer.save()


def list_single_column_values(file_name, column_name, file_url=working_file_url):
    """
    list a single column's all values
    :param file_name: the file name to be handled (all files should be stored in file_directions.working_file_url)
    :param column_name: the column name to be handled
    :param file_url:
    :return: a list of column values
    """
    data = pandas.read_excel(file_url + file_name)

    dropped_data = data.drop_duplicates(subset=[column_name], keep='first')
    return dropped_data[column_name].tolist()


def list_file_columns_values(file_name, file_url=working_file_url):
    """

    :param file_name:
    :param file_url:
    :return:
    """
    columns_dict = {}
    data = pandas.read_excel(file_url + file_name)
    for column in data.columns:
        print ('column:%s' % column)
        if list(data.columns).index(column) == 0:  # ignore the first column -- the number of company
            continue
        dropped_data = data.drop_duplicates(subset=[column], keep='first')
        # if dropped_data.size > 1000:
        #     column_dict = {column: ['varied']}
        # else:
        #     column_dict = {column: dropped_data[column].tolist()}
        sort_list = dropped_data[column].tolist()
        sort_list.sort()
        sort_list.insert(0, 'Nan Percent')
        sort_list.insert(0, 'Total Num')
        count_list = []
        for item in sort_list:
            if item == 'Total Num':
                count_list.append(data.__len__())
            elif item == 'Nan Percent':
                count_list.append(float(float(data[column].isna().sum()) / float(data[column].__len__())))
            elif item is numpy.nan:
                count_list.append(data[column].isna().sum())
            elif isinstance(item, unicode):
                counted_data = data[data[column] == item.encode('utf-8')]
                count_list.append(counted_data.__len__())
            else:
                count_list.append(data[data[column] == item].__len__())
        column_dict = {column: sort_list}
        count_dict = {column + '_count': count_list}
        columns_dict.update(column_dict)
        columns_dict.update(count_dict)

    return columns_dict


def list_category_columns_values(category, category_name, file_url=categorized_data_file_url):
    """

    :param category:
    :param category_name:
    :param file_url:
    :return:
    """

    wb = xlsxwt.Workbook(file_utils.check_file_url(categorized_data_file_url) + category_name + '.xlsx',
                         {'nan_inf_to_errors': True})
    # writer = pandas.ExcelWriter(unicode(file_utils.check_file_url(categorized_data_file_url) + category_name + '.xlsx'))
    for file_name in category:
        print (file_name)
        ws = wb.add_worksheet(unicode(file_name))
        cols_dict = list_file_columns_values(unicode(file_name) + '.xlsx', file_url=file_url)
        index_column = 0
        cols_sort_keys = cols_dict.keys()
        cols_sort_keys.sort()
        for key in cols_sort_keys:
            index_row = 0
            ws.write(index_row, index_column, key)
            for item in cols_dict.get(key):
                index_row += 1
                ws.write(index_row, index_column, item)

            index_column += 1

    wb.close()
    return


def rearrange_annual_report_share_holder_info():
    """
    年报-股东（发起人）及出资信息.xlsx has two columns need to be rearranged -- 认缴出资信息 and 实缴出资信息,
     they can be divided into three parts separately.
    :return:
    """
    table = xlrd.open_workbook(filename=working_file_url + u'年报-股东（发起人）及出资信息.xlsx').sheet_by_name('Sheet')
    wb = xlsxwt.Workbook(working_file_url + u'年报-股东（发起人）及出资信息_rearranged.xlsx')
    ws = wb.add_worksheet('Sheet')
    for index_row in range(0, table.nrows):
        write_index_col = 0
        head_wrote = index_row > 2
        for index_col in range(0, table.ncols):
            if index_col == 3 or index_col == 4:
                item_str = str(table.cell_value(index_row, index_col))
                items = item_str.split()
                if items.__len__() == 3:
                    for i in range(0, 3):
                        sepa_item = items[i].split(u'：')
                        if sepa_item.__len__() > 1:
                            if not head_wrote:
                                ws.write(0, write_index_col, sepa_item[0])
                            ws.write(index_row, write_index_col, sepa_item[1])
                        write_index_col += 1
                elif index_row == 0:
                    write_index_col += 3
                else:
                    print('split error at row:%d, col:%d, info:%s' % (
                        index_row, index_col, str(table.cell_value(index_row, index_col))))
                    write_index_col += 3
            else:
                ws.write(index_row, write_index_col, table.cell_value(index_row, index_col))
                write_index_col += 1
    wb.close()


# print(list_category_columns_values(category_annual_report_files, u'年报类'))
# print(rearrange_annual_report_share_holder_info())
