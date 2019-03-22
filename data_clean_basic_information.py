# *- coding:utf-8 -*-

"""
 module for annual reports data clean.
 including:
    工商基本信息表
    海关进出口信用
    招投标
    债券信息
    融资信息

 Empty values are mostly replaced by -1.
"""

import data_clean_utils as dcu
import file_utils
import primary_analysis as panaly
from file_directions import clean_data_temp_file_url
from files_category_info import category_basic_information


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_basic_information, u'基本信息类')


#  TODO handle all the duplicate data in all tables listed in '基本信息类'


def duplicate_handle():
    for name in category_basic_information:
        dcu.merge_rows(name + '.xlsx')



def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_basic_information, u'基本信息类_dup_handled',
                                        file_url=clean_data_temp_file_url)



print(duplicate_handle())