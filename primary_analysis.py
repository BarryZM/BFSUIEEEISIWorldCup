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
from file_directions import origin_file_url, working_file_url, statistic_data_file_url, categorized_data_file_url, \
    clean_data_temp_file_url

reload(sys)
sys.setdefaultencoding('utf-8')


def data_excel_statistic_info(file_name, init_file_dir=origin_file_url, work_file_dir=working_file_url):
    """
    get the simple statistic info for one data file, the info will be stored under statistic_data_file_url with the
    same file name with file_name, every sheet is one column's info with sheet name be the column's name.
    :param work_file_dir:
    :param init_file_dir:
    :param file_name: the file name of the excel, e.g. data.xls
    :return:
    """
    init_file = init_file_dir + file_name

    if work_file_dir is not None:
        work_file = work_file_dir + file_name
        file_utils.copy_file(init_file, work_file)
        print ('copy file: ' + file_name)

    print (init_file)
    data = file_utils.read_file_to_df(init_file_dir, file_name)

    writer = pandas.ExcelWriter(unicode(file_utils.check_file_url(statistic_data_file_url) + file_name))
    for column in data.columns:
        described_data = data[column].describe()
        print (described_data)
        # to name a sheet, there's some rules need to adopt
        m = openpyxl_child.INVALID_TITLE_REGEX.search(column)
        if m:
            for item in m.group():
                scolumn = column.encode('utf-8').replace(item.encode('utf-8'), '-')
                column = scolumn
        if len(unicode(column)) > 10:
            column = unicode(column)[0:10]
        file_utils.write_file_without_save(described_data, writer, sheet_name=column, index=True)
    writer.save()


def describe_file_folder(file_holder_url, copy_file_dir=None):
    """
    get simple statistic info for all data files in specific file holder
    :param copy_file_dir:
    :param file_holder_url: the folder direction to be described
    :return:
    """
    for file_name in os.listdir(file_holder_url):
        if file_name.startswith('.'):  # ignore .DS_Store
            continue
        data_excel_statistic_info(file_name, init_file_dir=file_holder_url, work_file_dir=copy_file_dir)


def describe_work():
    """
    get simple statistic info for all data files in our problem
    :return:
    """
    describe_file_folder(origin_file_url, working_file_url)


def describe_clean_work():
    """
    get simple statistic info for all data files in our problem
    :return:
    """
    describe_file_folder(clean_data_temp_file_url)


def data_categorize():
    """
    categorize these tables
    :return:
    """
    file_name = u'数据初整理'
    new_file_name = u'categorize数据初整理.xlsx'
    data = file_utils.read_file_to_df('', file_name, sheet_name='data')
    categorize_info = file_utils.read_file_to_df('', file_name, sheet_name='categorize')
    writer = pandas.ExcelWriter(new_file_name)
    for column in categorize_info.columns:
        categorized_data = pandas.DataFrame(columns=data.columns.tolist())
        for row in data.itertuples():
            if categorize_info[column].tolist().__contains__(row[1]):
                row_data = [list(row[1:len(row)])]
                categorized_data = pandas.concat(
                    [categorized_data, pandas.DataFrame(row_data, columns=data.columns.tolist())], ignore_index=True)
        file_utils.write_file_without_save(categorized_data, writer, sheet_name=column, index=False)

    writer.save()


def list_single_column_values(file_name, column_name, file_url=working_file_url):
    """
    list a single column's all values
    :param file_name: the file name to be handled (all files should be stored in file_directions.working_file_url)
    :param column_name: the column name to be handled
    :param file_url:
    :return: a list of column values
    """
    data = file_utils.read_file_to_df(file_url, file_name)

    dropped_data = data.drop_duplicates(subset=[column_name], keep='first')
    return dropped_data[column_name].tolist()


def list_file_columns_values(file_name, file_url=working_file_url):
    """

    :param file_name:
    :param file_url:
    :return:
    """
    columns_dict = {}
    data = file_utils.read_file_to_df(file_url, file_name)
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
                try:
                    count_list.append(float(float(data[column].isna().sum()) / float(data[column].__len__())))
                except AttributeError as ae:
                    count_list.append(0)
            elif item is numpy.nan:
                try:
                    count_list.append(data[column].isna().sum())
                except AttributeError as ae:
                    count_list.append(0)
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


def list_category_columns_values(category, category_name, file_url=working_file_url):
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
        cols_dict = list_file_columns_values(unicode(file_name), file_url=file_url)
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

def comments_generate():
    """
    generate comments for each table's dirty value handle
    :return:
    """
    comment_str_ori = u"\
    Dirty value handle for table {$$}.\n\
    First we'll drop rows that empty value is too many.\n\
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']\n\
    # Once there are more than 3 empties in these 8 columns we will drop that row.\n\
    Then we check nulls column by column and decide how to process with it.\n\
    Next we should numeric all the value for future process.\n\
    After these are done, it's time to work out features we can use in this table which belongs\n\
        to exploratory data analysis. \n\
".encode('utf-8')
    column_str_ori = "\n\
    -----------------------------\n\
    {$$$}\n\
    ------\n"
    for file_name in os.listdir(working_file_url):
        comment_str = comment_str_ori.replace('{$$}', file_name.encode('utf-8'))
        df = file_utils.read_file_to_df(working_file_url, file_name)
        column_list = df.columns.tolist()
        for i in range(1, len(column_list)):
            comment_str += column_str_ori.replace('{$$$}', column_list[i].encode('utf-8'))

        comment_str += '\n    -----------------------------'
        with open(file_utils.check_file_url('dirty_value_handle_comments/') + file_name + '_comments.txt', 'w+') as f:
            f.write(comment_str)
    return
