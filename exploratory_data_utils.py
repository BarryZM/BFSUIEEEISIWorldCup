# *- coding:utf-8 -*-

"""
 Exploratory data utils
"""
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def category_mapping(df_temp, columns, map, unknown=-1, others=-1):
    """
    map categories into numbers
    :type map: dict
    """
    row_list = []

    for column in columns:
        if len(df_temp[column]) > 0:
            item_temp = df_temp[column].reset_index().at[0, column]
            if item_temp in map.keys():
                for key in map.keys():
                    if item_temp == key:
                        row_list.append(map.get(key))
                        break
            else:
                row_list.append(others)
        else:
            row_list.append(unknown)

    return row_list


def category_count(df_temp, column, map):
    """
    count categories numbers
    :type map: dict
    """
    row_list = []

    if len(df_temp[column]) > 0:
        item_temp = df_temp[column].reset_index().at[0, column]
        if item_temp in map.keys():
            for key in map.keys():
                if item_temp == key:
                    row_list.append(map.get(key))
                    break
        else:
            row_list.append(others)

    return row_list
