# *- coding:utf-8 -*-

"""
 module for soft assets data clean.
 including:
    专利
    产品
    作品著作权
    商标
    资质认证
    软著著作权
    项目信息
"""

import data_clean_utils as dcu
import file_utils
import primary_analysis as panaly
from file_directions import clean_data_temp_file_url
from files_category_info import category_soft_assets_files
import pandas


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_soft_assets_files, u'软资产类')


def duplicate_handle():
    for name in category_soft_assets_files:
        dcu.merge_rows(name + '.xlsx')


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_soft_assets_files, u'软资产类_dup_handled',
                                        file_url=clean_data_temp_file_url)
    return


# def work():
#     raw_files_primary_analysis()
#     duplicate_handle()
#     primary_analysis_after_duplicate_handled()

def empty_value_handle_patent():
    """

    :return:
    """
    dcu.drop_unit(u'专利', u'授权公告日'.encode('utf-8'), [u'同一申请的已公布的文献号', '-'], empty_mask='1000-01-01')
    dcu.drop_prefix_unit(u'专利', u'申请日'.encode('utf-8'), [u'公告日：'], empty_mask='1000-01-01')
    dcu.drop_unit(u'专利', u'申请日'.encode('utf-8'), ['-'], empty_mask='1000-01-01')

    panaly.list_category_columns_values([u'专利'], u'专利_empty_handled',
                                        file_url=clean_data_temp_file_url)
    return


def empty_value_handle_work():
    """

    :return:
    """
    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'作品著作权')
    values = {u'作品著作权类别'.encode('utf-8'): 9, u'作品著作权登记日期'.encode('utf-8'): '1000-01-01',
              u'作品著作权创作完成日期'.encode('utf-8'): '1000-01-01', u'作品著作权首次发布日期'.encode('utf-8'): '1000-01-01'}
    df = df.fillna(values)
    file_utils.write_file(df, clean_data_temp_file_url, u'作品著作权')

    status_1 = [u'A 文字', u'文字', u'文字作品']
    status_2 = [u'B 音乐', u'音乐', u'音乐作品']
    status_3 = [u'F 美术', u'美术', u'美术作品']
    status_4 = [u'G 摄影', u'摄影', u'摄影作品']
    status_5 = [u'H 电影', u'电影', u'电影作品和类似摄制电影的方法创造的作品', u'电影和类似摄制电影方法创作的作品', u'I 类似摄制电影方法创作作品', u'类似摄制电影方法创作的作品']
    status_6 = [u'J 工程设计图、产品设计图', u'工程设计图、产品设计图', u'工程设计图、产品设计图作品', u'建筑']
    status_7 = [u'K 地图、示意图', u'地图、示意图', u'图形']
    status_8 = [9]
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8]
    status_after = [1, 2, 3, 4, 5, 6, 7, 9]

    dcu.merge_status(u'作品著作权', u'作品著作权类别'.encode('utf-8'), status_list, status_after, others=8)

    # TODO Other columns
    return


def empty_value_handle_trademark():
    """
    Dirty value handle for table 商标.xlsx.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    商标状态
    ------
    Empty percentage is 0.2597%(367 out of 141312). We replace them as 'Unknown'.

    -----------------------------
    申请日期
    ------
    Empty percentage is 0.3637%(514 out of 141312). We replace with '1000-01-01'.
    Others are well formatted.

    -----------------------------
    专用权期限开始日期
    ------
    All empty, drop it.

    -----------------------------
    专用权期限结束日期
    ------
    Empty percentage is 21.4922%(30371 out of 141312). This column's value can be extract from '商标使用期限时间段', so we
    drop it.
    -----------------------------
    商标使用期限时间段
    ------
    Empty percentage is 1.5915%(2249 out of 141312). We map them to '1000-01-01至1000-01-01'.
    Others are well formatted except some are '至', for these value we change to '1000-01-01至1000-01-01'.

    -----------------------------
    :return:
    """
    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'商标')
    values = {u'商标状态'.encode('utf-8'): 'Unknown', u'申请日期'.encode('utf-8'): '1000-01-01',
              u'商标使用期限时间段'.encode('utf-8'): u'1000-01-01至1000-01-01'}
    df = df.fillna(values)
    file_utils.write_file(df, clean_data_temp_file_url, u'商标')

    dcu.drop_columns(u'商标', [u'专用权期限开始日期'.encode('utf-8')])
    dcu.drop_columns(u'商标', [u'专用权期限结束日期'.encode('utf-8')])

    status_1 = [u'至']
    status_list = [status_1]
    status_after = [u'1000-01-01至1000-01-01']

    dcu.merge_status(u'商标', u'商标使用期限时间段'.encode('utf-8'), status_list, status_after)
    return


def empty_value_handle_copyright():
    """
    Dirty value handle for table 软著著作权.xlsx.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    软件全称
    ------
    Nothing to do with it.

    -----------------------------
    软件著作权版本号
    ------
    Nothing to do with it.

    -----------------------------
    软件著作权登记批准日期
    ------
    Make time well formatted.

    -----------------------------
    :return:
    """
    dcu.time_unicode_format(u'软著著作权', u'软件著作权登记批准日期'.encode('utf-8'))


def primary_analysis_after_empty_handled():
    """
    primary analysis after empty data handled
    :return:
    """
    panaly.list_category_columns_values(category_soft_assets_files, u'软资产类_empty_handled',
                                        file_url=clean_data_temp_file_url)
    return
