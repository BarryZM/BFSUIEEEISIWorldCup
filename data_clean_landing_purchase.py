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


# def empty_value_handle_basic_info():
#     """
#     empty_value handle for table 年报-企业基本信息.
#     :return:
#     """
#     empty_check_list = [u'行政区',
#                         u'土地用途',
#                         u'成交价（万元）']
#     dcu.drop_rows_too_many_empty(u'购地-地块公示', columns=empty_check_list, thresh=2)
#     # panaly.list_category_columns_values([u'购地-地块公示'], u'购地-地块公示_empty_handled',
#     #                                     file_url=clean_data_temp_file_url)
#     return


def time_rearranged(file_name, column_name):

    # 用split分开时间， 注意：之后数据分析所要用时间表头为0（数字格式）
    df = fu.read_file_to_df(clean_data_temp_file_url, file_name, sheet_name='Sheet')  # 读取工作表
    df["time"], df["minute"], df["day"] = df[column_name].str.split(" ", n=1).str  # 分成两个表 n为劈开的次数
    df.drop(column_name, axis=1, inplace=True)  # 删除原有的列
    df.drop("minute", axis=1, inplace=True)  #删除具体时间
    fu.write_file(df, clean_data_temp_file_url, file_name, ext='.xlsx', sheet_name='Sheet', index=False)  # 保存

    # table = fu.read_file_to_df(clean_data_temp_file_url, file_name, sheet_name='Sheet')
    # wr1 = pd.concat([table, table[column_name].str.split(r' ', expand=True)], axis=1, names=['time','miniute'])
    # fu.write_file(wr1, clean_data_temp_file_url, file_name, ext='.xlsx',sheet_name='Sheet', index=False)
    #
    # dcu.drop_columns(file_name, 1 )
    return


def land_usage(file_name, column_name):
    status_5 = ['05','051','052','053','054', u'批发零售用地', u'住宿餐饮用地', u'商务金融用地',u'其他商服用地',u'商服用地',u'05、07']
    status_6 = [u'06', u'061', u'062', u'063', u'工业用地', u'采矿用地', u'仓储用地', u'工矿仓储用地']
    status_7 = [u'07', u'071', u'072',u'073',u'074',u'077',u'住宅用地', u'城镇住宅用地', u'农村宅基地', u'廉租住房用地',u'中低价位、中小套型普通商品住房用地',
                     u'其他住房用地',u'其他普通商品住房用地',u'经济适用住房用地',u'高档住宅用地',u'公共租赁住房用地']
    status_8 = [u'08', u'081', u'082', u'083', u'084', u'085',u'086',u'087',u'088',u'机关团体用地',u'新闻出版用地',u'新闻用地',
                     u'科教用地', u'医卫慈善用地', u'文体娱乐用地',u'公共设施用地',u'公园与绿地',u'风景名胜设施用地',u'公共管理与公共服务用地']
    status_9 = [u'09', u'091', u'092', u'093',u'094',u'095',u'军事设施用地', u'使领馆用地', u'监教场所用地',
                     u'宗教用地',u'殡葬用地',u'特殊用地']
    status_10 = [u'100', u'10', u'101', u'102', u'103', u'104', u'105', u'106', u'107', u'铁路用地', u'公路用地',
                     u'街巷用地', u'农村道路', u'机场用地', u'港口码头用地', u'管道运输用地',u'交通运输用地']
    status_11 = [u'11', u'111', u'112', u'113', u'114', u'115', u'116', u'117', u'118', u'119', u'河流水面',
                     u'湖泊水面', u'水库水面', u'坑塘水面', u'沿海滩涂', u'内陆滩涂', u'沟渠', u'水工建筑用地',
                     u'冰川及永久积雪',u'水域及水利设施用地']
    status_12 = [u'12', u'121', u'122', u'123', u'124', u'125', u'126', u'127', u'空闲地', u'设施农用地',
                     u'田坎', u'盐碱地', u'沼泽地', u'沙地', u'裸地',u'其他土地']
    status_no = [u'0',u'土地面积(公顷)'] #错误的类别
    status_list = [status_5, status_6, status_7, status_8, status_9, status_10, status_11, status_12, status_no]
    status_after = [5, 6, 7, 8, 9, 10, 11, 12, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return




def clean_gddkgs():
    time_rearranged(u'购地-地块公示', u'时间')

    file_name = u'购地-地块公示'
    dcu.drop_columns(file_name, u'行政区')
    dcu.drop_columns(file_name, u'出让年限')
    dcu.drop_columns(file_name, u'土地使用条件')

    dcu.merge_status(file_name, u'公示日期', [], [], empty_mask='-65535')


    # wr1 = fu.read_file_to_df(clean_data_temp_file_url, file_name, sheet_name='Sheet')
    # # wr1 = wr1.fillna({u'纳税人资格'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引
    #
    # fu.write_file(wr1, clean_data_temp_file_url,file_name, ext='.xlsx', sheet_name='Sheet', index=False)

    land_usage(u'购地-地块公示', u'土地用途')

    return

    # AB =1 CD =2
    # status_1 = [u'A', u'B']
    # status_2 = [u'C', u'D']
    # status_list = [status_1,status_2]
    # status_after = [1,2]
    # dcu.merge_status('temp', 'a',status_list, status_after)

#把土地用途转换为数字



'''
    Dirty value handle for table 购地-市场交易-土地抵押.xlsx.
    First we'll drop rows that empty value is too many.
    # ['抵押面积(公顷)','土地用途','抵押土地用途','抵押土地权属性质与使用权类型', '评估金额(万元)','抵押金额(万元)','土地抵押登记结束时间']
    # Once there are more than 3 empties in these 7 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    土地抵押人性质
    ------
    Empty percentage is 26.0%(8268 out of 31799).
    Empty values can be considered to 'Unknown'.
    As the values have many different types and and disturb us a lot. We decide to drop this column.
    -----------------------------
    抵押面积(公顷)
    ------
    Empty percentage is 19.7%(6253 out of 31799).
    Empty values can be considered to 'Unknown'.
    We consider each part as an independent status. and all of the values are showed by correct format, so we can use them directly.
    -----------------------------
    土地用途
    ------
    Empty percentage is 0.02%(7 out of 31799).
    Empty values can be considered to 'Unknown'.
    62 status in this value has, but some of them are the code of the status, and some values is the small type of the
    huge status. So we conclude them by using '土地分类代码表'. So we can map them in to 13 status:
    {'商服用地':5,'工矿仓储用地':6,'住宅用地':7,'公共管理与公共服务用地':8,'特殊用地':9,'交通运输用地':10,'水域及水利设施用地':11,'其它土地':12,'Unknown':-1}
    -----------------------------
    抵押土地用途
    ------
    Empty percentage is 19.7%(6260 out of 31799).
    Empty values can be considered to 'Unknown'.
    62 status in this value has, but some of them are the code of the status, and some values is the small type of the
    huge status. So we conclude them by using '土地分类代码表'. So we can map them in to 13 status:
    {'商服用地':5,'工矿仓储用地':6,'住宅用地':7,'公共管理与公共服务用地':8,'特殊用地':9,'交通运输用地':10,'水域及水利设施用地':11,'其它土地':12,'Unknown':-1}
    -----------------------------
    抵押土地权属性质与使用权类型
    ------
    Empty percentage is 21.43%(6816 out of 31799).
    Empty values can be considered to 'Unknown'.
    When we analyze these data, we focus on the ownership of the land, so we use the key point['国有','集体'], others include in 'others'
    So we conclude them by using {'国有':1,'集体':2,'其他':3,'Unknown':-1}
    -----------------------------
    土地面积
    ------
    Empty percentage is 0.00%(1 out of 31799).
    Empty values can be considered to 'Unknown'.
    The empty value accounts for a small scale, so we can drop that empty value.
    -----------------------------
    评估金额(万元)
    ------
    Empty percentage is 22.5%(7154 out of 31799).
    Empty values can be considered to 'Unknown'.
    We consider each part as an independent status. and all of the values are showed by correct format, so we can use them directly.
    -----------------------------
    抵押金额(万元)
    ------
    Empty percentage is 19.7%(6276 out of 31799).
    Empty values can be considered to 'Unknown'.
    We consider each part as an independent status. and all of the values are showed by correct format, so we can use them directly.
    -----------------------------
    土地抵押登记起始时间
    ------
    Empty percentage is 0%(0 out of 31799)..
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    However, some time data has the exact time value that are not needed. So we just delete the exact time.
    -----------------------------
    土地抵押登记结束时间
    ------
    Empty percentage is 19.7%(6258 out of 31799).
    Empty values can be considered to 'Unknown'.
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    However, some time data has the exact time value that are not needed. So we just delete the exact time.
    -----------------------------


'''

def empty_value_handle_gdscjytddy():
    """
    empty_value handle for table
    :return:
    """
    empty_check_list = [u'抵押面积(公顷)'.encode('utf-8'),
                        u'土地用途'.encode('utf-8'),
                        u'抵押土地用途'.encode('utf-8'),
                        u'抵押土地权属性质与使用权类型'.encode('utf-8'),
                        u'评估金额(万元)'.encode('utf-8'),
                        u'抵押金额(万元)'.encode('utf-8'),
                        u'土地抵押登记结束时间'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'购地-市场交易-土地抵押.xlsx', columns=empty_check_list, thresh=3)
    # panaly.list_category_columns_values([u'购地-市场交易-土地抵押'], u'购地-市场交易-土地抵押_empty_handled',
    #                                     file_url=clean_data_temp_file_url)
    return



def clean_gdscjytddy():
    file_name = u'购地-市场交易-土地抵押'

    time_rearranged(file_name, u'土地抵押登记起始时间')  # 两种时间会被分割为0和0.1的表头
    time_rearranged(file_name, u'土地抵押登记结束时间')

    dcu.drop_columns(file_name, u'土地抵押人性质')

    dcu.merge_status(file_name, u'抵押面积(公顷)', [], [], empty_mask='-65535')
    dcu.merge_status(file_name, u'土地面积', [], [], empty_mask='-65535')
    dcu.merge_status(file_name, u'评估金额(万元)', [], [], empty_mask='-65535')
    dcu.merge_status(file_name, u'抵押金额(万元)', [], [], empty_mask='-65535')

    land_usage(file_name, u'土地用途')
    land_usage(file_name, u'抵押土地用途')

    dcu.extract_keyword(file_name, u'抵押土地权属性质与使用权类型', [u'国有', u'集体'], empty_mask='Unknown', others_mask='Others')

    return

# import data_clean_utils as dcu
# file_name = u'购地-市场交易-土地抵押_test'
# dcu.extract_keyword(file_name, u'抵押土地权属性质与使用权类型', u'国有',u'集体',empty_mask='Unknown', others_mask='Others')



'''
    Dirty value handle for table 购地-市场交易-土地转让.xlsx.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    成交时间
    ------
    Empty percentage is 0%(0 out of 31554).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    However, some time data has the exact time value that are not needed. So we just delete the exact time.
    -----------------------------
    土地面积(公顷)
    ------
    Empty percentage is 0.00%(1 out of 31554).
    Empty values can be considered to 'Unknown'.
    The empty value accounts for a small scale, so we can drop that empty value.
    -----------------------------
    土地用途
    ------
    Empty percentage is 0.02%(7 out of 31554).
    Empty values can be considered to 'Unknown'.
    62 status in this value has, but some of them are the code of the status, and some values is the small type of the
    huge status. So we conclude them by using '土地分类代码表'. So we can map them in to 13 status:
    {'商服用地':5,'工矿仓储用地':6,'住宅用地':7,'公共管理与公共服务用地':8,'特殊用地':9,'交通运输用地':10,'水域及水利设施用地':11,'其它土地':12,'Unknown':-1}
    -----------------------------
    土地使用年限
    ------
    Empty percentage is 96.5%(7 out of 31554).
    Empty values can be considered to 'Unknown'.
    Since the empty value accounts for a large scale, we decide to drop this column.
    -----------------------------
    土地级别
    ------
    Empty percentage is 95.9%(30263 out of 31554).
    Empty values can be considered to 'Unknown'.
    Since the empty value accounts for a large scale, we decide to drop this column.
    -----------------------------
    土地使用权类型
    ------
    Empty percentage is 97.4%(30720 out of 31554).
    Empty values can be considered to 'Unknown'.
    Since the empty value accounts for a large scale, we decide to drop this column.
    -----------------------------
    土地利用状况
    ------
    Empty percentage is 94.0%(29668 out of 31554).
    Empty values can be considered to 'Unknown'.
    Since the empty value accounts for a large scale, we decide to drop this column.
    -----------------------------
    转让方式
    ------
    Empty percentage is 97.3%(30697 out of 31554).
    Empty values can be considered to 'Unknown'.
    Since the empty value accounts for a large scale, we decide to drop this column.
    -----------------------------
    转让价格(万元)
    ------
    Empty percentage is 97.3%(30697 out of 31554).
    Empty values can be considered to 'Unknown'.
    Since the empty value accounts for a large scale, we decide to drop this column.
    -----------------------------
'''

# def empty_value_handle_gdscjytdzr():
#     """
#     empty_value handle for table
#     :return:
#     """
#     empty_check_list = [u'成交时间'.encode('utf-8'),
#                         u'土地面积'.encode('utf-8'),
#                         u'土地用途'.encode('utf-8')]
#     dcu.drop_rows_too_many_empty(u'购地-市场交易-土地转让.xlsx', columns=empty_check_list, thresh=2)
#     # panaly.list_category_columns_values([u'购地-市场交易-土地转让'], u'购地-市场交易-土地转让_empty_handled',
#     #                                     file_url=clean_data_temp_file_url)
#     return


def clean_gdscjytdzr():
    file_name = u'购地-市场交易-土地转让'
    time_rearranged(file_name, u'成交时间'.encode('utf-8'))

    # 时间会被分割为0的表头

    dcu.drop_columns(file_name, u'土地使用年限')
    dcu.drop_columns(file_name, u'土地级别')
    dcu.drop_columns(file_name, u'土地使用权类型')
    dcu.drop_columns(file_name, u'土地利用状况')
    dcu.drop_columns(file_name, u'转让方式')
    dcu.drop_columns(file_name, u'转让价格(万元)')

    dcu.merge_status(file_name, u'土地面积(公顷)', [], [], empty_mask='-65535')

    land_usage(file_name, u'土地用途')

    return


# file_name = u'购地-市场交易-土地转让_test'
# dclp.time_rearranged(u'购地-市场交易-土地转让_test', u'成交时间'.encode('utf-8'))  # 时间会被分割为0的表头


# reload(data_clean_landing_purchase)


def data_clean_landing_purchase_fdcdqygdqk():
    """
        Dirty value handle for table 购地-房地产大企业购地情况.xlsx.
        First we'll drop rows that empty value is too many.
        # ['行政区','签订日期','供地总面积（公顷）','约定动工时间', '土地用途','供应方式','最小容积率','最大容积率',
        '成交价款（万元）','约定竣工时间']

        -----------------------------
        行政区
        ------
        drop
        -----------------------------
        签订日期
        ------
        no change
        -----------------------------
        供地总面积（公顷）
        ------
        turn null into 'Unknown'
        -----------------------------
        约定动工时间
        ------
        95% null, turn null into 'Unknown'
        -----------------------------
        土地用途
        ------
        turn into several integers
        -----------------------------
        供应方式
        ------
        95% null, turn null into 'Unknown',turn into several integers
        -----------------------------
        最小容积率
        ------
        98% null, turn null into 'Unknown'
        -----------------------------
        最大容积率
        ------
        98% null, turn null into 'Unknown'
        -----------------------------
        成交价款（万元）
        ------
        turn null into 'Unknown'
        -----------------------------
        约定竣工时间
        ------
        98% null, turn null into 'Unknown'
        -----------------------------
        """
    dcu.drop_columns(u'购地-房地产大企业购地情况', u'行政区')  # 删除行政区
    # 日期：需要去掉小数部分

    land_usage(u'购地-房地产大企业购地情况', u'土地用途')  # 土地用途分类

    dcu.merge_status(u'购地-房地产大企业购地情况', u'供地总面积（公顷）', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大企业购地情况', u'约定动工时间',[],[])
    dcu.merge_status(u'购地-房地产大企业购地情况', u'最小容积率', [], [],empty_mask='-65535')  # 空值处理
    dcu.merge_status(u'购地-房地产大企业购地情况', u'最大容积率', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大企业购地情况', u'成交价款（万元）', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大企业购地情况', u'约定竣工时间', [], [])
    dcu.merge_status(u'购地-房地产大企业购地情况', u'供应方式', [[u'划拨'],[u'协议出让'],[u'拍卖出让'],[u'招标出让'],[u'挂牌出让']], [1,2,3,4,5])
    return


def data_clean_landing_purchase_fdcddkcrqk():
    """
                Dirty value handle for table 购地-房地产大地块出让情况.xlsx.
        First we'll drop rows that empty value is too many.
        ['签订日期','供地总面积','约定动工时间', '土地用途','供应方式','容积率下限','容积率上限',
        '成交价款（万元）','约定竣工时间']

        -----------------------------
        签订日期
        ------
        turn into integer
        -----------------------------
        供地总面积
        ------
        turn null into 'Unknown'
        -----------------------------
        约定动工时间
        ------
        97% null, turn null into 'Unknown'
        -----------------------------
        土地用途
        ------
        turn into several integers
        -----------------------------
        供应方式
        ------
        97% null, turn null into 'Unknown',turn into several integers
        -----------------------------
        容积率下限
        ------
        98% null, turn null into 'Unknown'
        -----------------------------
        容积率上限
        ------
        98% null, turn null into 'Unknown'
        -----------------------------
        成交价款（万元）
        ------
        86% null, turn null into 'Unknown'
        -----------------------------
        约定竣工时间
        ------
        99% null, turn null into 'Unknown'
        -----------------------------
        """
    dcu.drop_columns(u'购地-房地产大地块出让情况', u'行政区')
    # 日期：需要去掉小数部分

    land_usage(u'购地-房地产大地块出让情况', u'土地用途')

    dcu.merge_status(u'购地-房地产大地块出让情况', u'供地总面积', [], [])
    dcu.merge_status(u'购地-房地产大企业购地情况', u'约定动工时间',[],[])   # 其他空值unknown
    dcu.merge_status(u'购地-房地产大企业购地情况', u'最小容积率', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大企业购地情况', u'最大容积率', [], [],empty_mask='-65535')   # 其他空值unknown
    dcu.merge_status(u'购地-房地产大企业购地情况', u'成交价款（万元）', [], [],empty_mask='-65535') # 数值型空值-665535
    dcu.merge_status(u'购地-房地产大企业购地情况', u'约定竣工时间', [], [])
    dcu.merge_status(u'购地-房地产大企业购地情况', u'供应方式', [[u'划拨'],[u'协议出让'],[u'拍卖出让'],[u'招标出让'],[u'挂牌出让']], [1,2,3,4,5])

    dcu.merge_status(u'购地-房地产大地块出让情况', u'供地总面积', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大地块出让情况', u'约定动工时间',[],[])
    dcu.merge_status(u'购地-房地产大地块出让情况', u'容积率下限', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大地块出让情况', u'容积率上限', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大地块出让情况', u'成交价款（万元）', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-房地产大地块出让情况', u'约定竣工时间', [], [])
    dcu.merge_status(u'购地-房地产大地块出让情况', u'供应方式', [[u'划拨'],[u'协议出让'],[u'拍卖出让'],[u'招标出让'],[u'挂牌出让']], [1,2,3,4,5])
    return

    land_usage(u'购地-房地产大地块出让情况',u'土地用途')
def data_clean_landing_purchase_jggg():
    """
                Dirty value handle for table 购地-结果公告.xlsx.
        First we'll drop rows that empty value is too many.
        ['总面积','土地用途','供应方式','签订日期','土地来源','土地使用年限','行业分类','土地级别','成交价格（万元）',
        '约定容积率上限','约定容积率下限','约定交地时间','约定开工时间','约定竣工时间','实际开工时间','实际竣工时间','批准单位']

        -----------------------------
        总面积
        ------
        turn null into 'Unknown'
        -----------------------------
        土地用途
        ------
        turn into several integers
        -----------------------------
        供应方式
        ------
        97% null,  turn null into 'Unknown',turn into several integers
        -----------------------------
        签订日期
        ------
        turn into integers
        -----------------------------
        土地来源
        ------
        99% null,drop
        -----------------------------
        土地使用年限
        ------
        96% null, turn null into 'Unknown', clean wrong numbers
        -----------------------------
        行业分类
        ------
        99% null, drop
        -----------------------------
        土地级别
        ------
        the smaller the number, the more expensive the land, 96% null
        -----------------------------
        成交价格（万元）
        ------
        86% null, turn null into 'Unknown'

        -----------------------------
        约定容积率上限
        ------
        99% null, turn null into 'Unknown'
        -----------------------------
        约定容积率下限
        ------
        99% null, turn null into 'Unknown'
        -----------------------------
        约定交地时间
        ------
        99% null, turn into integers
        -----------------------------
        约定开工时间
        ------
        97% null, turn into integers
        -----------------------------
        约定竣工时间
        ------
        99% null, turn into integers
        -----------------------------
        实际开工时间
        ------
        100% null, drop
        -----------------------------
        实际竣工时间
        ------
        100% null, drop
        -----------------------------
        批准单位
        ------
        99% null, drop
        -----------------------------
        """
    dcu.drop_columns(u'购地-结果公告', u'土地来源')
    dcu.drop_columns(u'购地-结果公告', u'土地使用年限')
    dcu.drop_columns(u'购地-结果公告', u'行业分类')
    dcu.drop_columns(u'购地-结果公告', u'土地级别')
    dcu.drop_columns(u'购地-结果公告', u'实际开工时间')
    dcu.drop_columns(u'购地-结果公告', u'实际竣工时间')
    dcu.drop_columns(u'购地-结果公告', u'批准单位')

    # 签订日期：需要去掉小数部分

    land_usage(u'购地-结果公告', u'土地用途')

    dcu.merge_status(u'购地-结果公告', u'总面积', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-结果公告', u'成交价格（万元）', [], [], empty_mask='-65535')
    dcu.merge_status(u'购地-结果公告', u'约定容积率上限', [], [],empty_mask='-65535')
    dcu.merge_status(u'购地-结果公告', u'约定容积率下限', [], [],empty_mask='-65535')

    dcu.merge_status(u'购地-结果公告', u'约定交地时间', [], [])
    dcu.merge_status(u'购地-结果公告', u'约定开工时间', [], [])
    dcu.merge_status(u'购地-结果公告', u'约定竣工时间', [], [])
    dcu.merge_status(u'购地-结果公告', u'供应方式', [[u'划拨'],[u'协议出让'],[u'拍卖出让'],[u'招标出让'],[u'挂牌出让']], [1,2,3,4,5])
    return

# data_clean_landing_purchase.data_clean_landing_purchase_fdcddkcrqk()


    # dcu.drop_columns(file_name, u'出让年限'.encode('utf-8'))
    #
    # return








