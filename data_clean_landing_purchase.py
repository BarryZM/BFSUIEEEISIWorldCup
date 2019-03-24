# *- coding:utf-8 -*-

"""
 module for landing purchase data clean.
 including:


 Empty values are mostly replaced by -1.
"""

import data_clean_utils as dcu
import file_utils as fu
import primary_analysis as panaly
from file_directions import clean_data_temp_file_url
from files_category_info import category_landing_purchase
import pandas as pd


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_landing_purchase, u'地产类')
    return


#  TODO handle all the duplicate data in all tables listed in '地产类'



def duplicate_handle(): # 该部分加入for循环进行了修改
    for name in category_landing_purchase:
        if name == category_landing_purchase:
            continue
        dcu.merge_rows(name + '.xlsx')

    return



def primary_analysis_after_duplicate_handled():

    panaly.list_category_columns_values(category_landing_purchase, u'地产类_dup_handled',
                                        file_url=clean_data_temp_file_url)
    return



'''
    Dirty value handle for table 购地-地块公示.xlsx.
    First we'll drop rows that empty value is too many.
    # ['行政区','土地用途','成交价（万元）']
    # Once there are more than 2 empties in these 3 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    行政区
    ------
    Empty percentage is 0.2%(37 out of 18192).
    Empty values can be considered to 'Unknown'.
    As the values have many different types and and disturb us a lot. We decide to drop this column.
    -----------------------------
    时间
    ------
    Empty percentage is 0%(0 out of 18192).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    However, some time data has the exact time value that are not needed. So we just delete the exact time.
    -----------------------------
    公示日期
    ------
    Empty percentage is 75.3%(13694 out of 18192).
    Empty values can be considered to 'Unknown'.
    We consider each part as an independent status. and all values with number are showed by correct format of time. So
    we can not change them anymore
    -----------------------------
    土地用途
    ------
    Empty percentage is 3%(6 out of 18192).
    Empty values can be considered to 'Unknown'.
    62 status in this value has, but some of them are the code of the status, and some values is the small type of the
    huge status. So we conclude them by using '土地分类代码表'. So we can map them in to 13 status:
    {'商服用地':5,'工矿仓储用地':6,'住宅用地':7,'公共管理与公共服务用地':8,'特殊用地':9,'交通运输用地':10,'水域及水利设施用地':11,'其它土地':12,'Unknown':-1}
    -----------------------------
    土地面积（公顷）
    ------
    Empty percentage is 0%(0 out of 18192).
    We consider each part as an independent status. and all of the values are showed by correct format, so we can use them directly.
    -----------------------------
    出让年限
    ------
    Empty percentage is 80.0%(14556 out of 18192).
    Empty values can be considered to 'Unknown'.
    As it have many empty values and the values exist have complicated format, so we choose to drop them.
    -----------------------------
    成交价（万元）
    ------
    Empty percentage is 76.1%(13840 out of 18192).
    Empty values can be considered to 'Unknown'.
    The existing values have the correct format of pure number, however, some values shows that the purchase price is 0.
    It's useless to use 0 to analyze the value of the company. so we conclude the value = 0 as 'Error'
    -----------------------------
    土地使用条件
    ------
    Empty percentage is 90.1%(16400 out of 18192).
    As it have many empty values and the values exist have complicated format, so we choose to drop them.
    -----------------------------
'''



def empty_value_handle_basic_info():
    """
    empty_value handle for table 年报-企业基本信息.
    :return:
    """
    empty_check_list = [u'行政区',
                        u'土地用途',
                        u'成交价（万元）']
    dcu.drop_rows_too_many_empty(u'一般纳税人.xlsx', columns=empty_check_list, thresh=2)
    # panaly.list_category_columns_values([u'一般纳税人'], u'一般纳税人_empty_handled',
    #                                     file_url=clean_data_temp_file_url)
    return


def time_rearranged():
    file_name = u'购地-地块公示_test'

    wr1 = fu.read_file_to_df(clean_data_temp_file_url, file_name,
                             sheet_name='Sheet')
    wr1 = wr1.fillna({u'时间'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引

    # wr2 = wr1[u'时间'.encode('utf-8')].str.split(' ',n = 1, expand = True ) # 使用split删除部分时间的精确时间
    wr2 = pd.merge(wr1, pd.DataFrame(wr1[u'时间'.encode('utf-8')].str.split(' ',n = 1, expand = True )),
                   how='left', left_index= True , right_index = True)
    wr3 = wr2.rename(columns={u'时间'.encode('utf-8'): 'time', '0': u'时间'.encode('utf-8')}, inplace=True)
    wr4 = wr3.rename(column = {'0': u'时间'.encode('utf-8')})
    fu.write_file(wr4, clean_data_temp_file_url, u'购地-地块公示_test', ext='.xlsx',
                  sheet_name='Sheet', index=False)

    dcu.drop_columns(file_name, 'time')
    dcu.drop_columns(file_name, '1')

    return



def clean_announcement_of_land():
    file_name = u'购地-地块公示_test'
    dcu.drop_columns(file_name, u'行政区'.encode('utf-8'))

    wr1 = fu.read_file_to_df(clean_data_temp_file_url, file_name,
                             sheet_name='Sheet')
    wr1 = wr1.fillna({u'纳税人资格': 'unknown'})  # 对空值进行处理以进行索引

    wr2 = wr1[u'时间'.encode('utf-8')].str.split(' ',n = 1, expand = False ) # 使用split删除部分时间的精确时间
    fu.write_file(wr2, clean_data_temp_file_url, u'购地-地块公示_test', ext='.xlsx',
                  sheet_name='Sheet', index=False)
    return

    # AB =1 CD =2
    # status_1 = [u'A', u'B']
    # status_2 = [u'C', u'D']
    # status_list = [status_1,status_2]
    # status_after = [1,2]
    # dcu.merge_status('temp', 'a',status_list, status_after)


def land_usage(file_name, column_name):
    status_5 = ['05','051','052','053','054',u'批发零售用地',u'住宿餐饮用地',u'商务金融用地',u'其它商服用地',u'商服用地',u'05、07']
    status_6 = [u'06', u'061', u'062', u'063', u'工业用地', u'采矿用地', u'仓储用地']
    status_7 = [u'07', u'071', u'072',u'073',u'住宅用地', u'城镇住宅用地', u'农村宅基地', u'中低价位、中小套型普通商品住房用地',
                     u'其他住房用地',u'其他普通商品住房用地',u'经济适用住房用地']
    status_8 = [u'08', u'081', u'082', u'083', u'084', u'085',u'086',u'087',u'088',u'机关团体用地',u'新闻出版用地'
                     u'科教用地', u'医卫慈善用地', u'文体娱乐用地',u'公共设施用地',u'公园与绿地',u'风景名胜设施用地']
    status_9 = [u'09', u'091', u'092', u'093',u'094',u'095',u'军事设施用地', u'使领馆用地', u'监教场所用地',
                     u'宗教用地',u'殡葬用地']
    status_10 = [u'100', u'10', u'101', u'102', u'103', u'104', u'105', u'106', u'107', u'铁路用地', u'公路用地',
                     u'街巷用地', u'农村道路', u'机场用地', u'港口码头用地', u'管道运输用地']
    status_11 = [u'11', u'111', u'112', u'113', u'114', u'115', u'116', u'117', u'118', u'119', u'河流水面',
                     u'湖泊水面', u'水库水面', u'坑塘水面', u'沿海滩涂', u'内陆滩涂', u'沟渠', u'水工建筑用地',
                     u'冰川及永久积雪']
    status_12 = [u'12', u'121', u'122', u'123', u'124', u'125', u'126', u'127', u'空闲地', u'设施农用地',
                     u'田坎', u'盐碱地', u'沼泽地', u'沙地', u'裸地']
    status_0 = [u'0']
    # status_list = [status_5, status_6, status_7, status_8, status_9, status_10, status_11, status_12, status_0]
    # status_after = [5, 6, 7, 8, 9, 10, 11, 12, 0]
    status_list = [status_5, status_6,status_7]
    status_after = [5, 6, 7]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return

import data_clean_landing_purchase
data_clean_landing_purchase.land_usage(u'购地-房地产大企业购地情况',u'土地用途')

    # info:
    # status_normal = [u'05、07']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'商服用地和住宅用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'05',u'051',u'052',u'053',u'054',u'批发零售用地',u'住宿餐饮用地',u'商务金融用地',u'其它商服用地']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'商服用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'06', u'061', u'062', u'063', u'工业用地', u'采矿用地', u'仓储用地']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'工矿仓储用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'07', u'071', u'072', u'城镇住宅用地', u'农村宅基地', u'中低价位、中小套型普通商品住房用地',
    #                  u'其他住房用地',u'其他普通商品住房用地',u'经济适用住房用地']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'住宅用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'08', u'081', u'082', u'083', u'084', u'085',u'086',u'087',u'088',u'机关团体用地',u'新闻出版用地'
    #                  u'科教用地', u'医卫慈善用地', u'文体娱乐用地',u'公共设施用地',u'公园与绿地',u'风景名胜设施用地']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'公共管理与公共服务用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'09', u'091', u'092', u'093',u'094',u'095',u'军事设施用地', u'使领馆用地', u'监教场所用地',
    #                  u'宗教用地',u'殡葬用地']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'特殊用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'100',u'10', u'101', u'102', u'103', u'104', u'105',u'106',u'107', u'铁路用地', u'公路用地',
    #                  u'街巷用地', u'农村道路',u'机场用地', u'港口码头用地', u'管道运输用地']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'交通运输用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'11', u'111', u'112', u'113', u'114', u'115', u'116', u'117', u'118', u'119',u'河流水面',
    #                  u'湖泊水面', u'水库水面', u'坑塘水面', u'沿海滩涂', u'内陆滩涂', u'沟渠',u'水工建筑用地',
    #                  u'冰川及永久积雪']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'水域及水利设施用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')
    #
    # status_normal = [u'12', u'121', u'122', u'123', u'124', u'125', u'126', u'127', u'空闲地', u'设施农用地',
    #                  u'田坎', u'盐碱地', u'沼泽地', u'沙地', u'裸地']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = [u'交通运输用地']  # 改成这个
    # dcu.merge_status(file_name, u'土地用途'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')

    # dcu.drop_columns(file_name, u'出让年限'.encode('utf-8'))
    #
    # return








