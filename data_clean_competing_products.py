# *- coding:utf-8 -*-

"""
 module for competing products data clean.
 including:


 Empty values are mostly replaced by -1.
"""

import data_clean_utils as dcu
import primary_analysis as panaly
from files_category_info import category_competing_products
from file_directions import clean_data_temp_file_url


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_competing_products, u'竞品')


# TODO handle all the duplicate data in all tables listed in '竞品'


def duplicate_handle():
    for name in category_competing_products:
        dcu.merge_rows(name + '.xlsx')


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_competing_products, u'竞品_dup_handled',
                                        file_url=clean_data_temp_file_url)


"""
    Dirty value handle for table 竞品
    First we'll drop rows that empty value is too many.
    ['竞品的标签','竞品轮次','竞品运营状态','竞品成立时间']
    Once there are more than 3 empties in these 4 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.
    -----------------------------
    竞品的行业
    ------
    Empty percentage is 94.0%(31400 out of 33388).
    27 status this value has, they are ['VR·AR','人工智能','企业服务','体育','光电','公共事业','农业','化工','医疗健康',
    '地产建筑','工具','房产家居','教育','文娱传媒','旅游','无人机','材料','汽车交通','消费生活','物流','环保','生产制造',
    '电商','硬件','社交','能源矿产','金融'].
    Though there are  lots of empty value in this part, It still be an important information for the future research.
    So we just add another status for the empty value:'Unknown'.
    -----------------------------

    竞品的标签
    ------
    Empty percentage is 0.02%(7 out of 33388).
    Considering that there are few empty columns in this part, we could choose to replace with 0 indicating we don't
    know the type of the product. What's more, we need to figure out that although it seems a mass to find out the kind
    in the existing values, it will be useful to guess what kind of industry did the company or the product lives in.
    -----------------------------

    竞品轮次
    ------
    Empty percentage is 30.9%(10314 out of 33388).
    35 status this value has, they are ['A轮','A+轮','B+轮','B轮','C+轮','C轮','D轮','E轮','E轮及以后','F轮','ICO','IPO'
    'IPO后','Pre-A','Pre-B','Pre-IPO','上市','主板定向增发','众筹','债券融资','后期阶段','天使轮','并购','战略合并','战略投资',
    '扶持资金','新三板','新三板定增','新四板','未知轮次','未融资','私有化','种子轮','股权转让','被收购'].
    As the values already have the kind about Unknown: We just add another status for the empty value:'未知轮次'.
    -----------------------------
    竞品详细地址
    ------
    Empty percentage is 7.2%(2404 out of 33388).
    As the values already have the kind about Unknown: We just add another status for the empty value:'未知'.
    And based on the counts for every status, we simplify these status to ['北京','上海','广州','深圳',,'杭州','国外'，'未知']
    So we can map these total 7 status to three: {'北京':0,'上海':1,'广州':2,'深圳':3,'杭州':4,'国外':5,'未知':-1}.
    -----------------------------
    竞品运营状态
    ------
    Empty percentage is 8.34%(2783 out of 33388).
    4 status can be concluded in this part, they are [‘停止更新’，‘已关闭’，‘融资中’，‘运营中’]
    We just add another status for the empty value:'Unknown'.
    So we can map these total 5 status to three: {‘停止更新’:0,‘已关闭’:1,融资中’:2,‘运营中’:3,'Unknown':-1}.
    -----------------------------
    竞品成立时间
    ------
    Empty percentage is 6.82%(2277 out of 33388).
    We consider each part as an independent status, for these empty value, we just add another status: 'Unknown'
    -----------------------------
"""


def industry(file_name, column_name):  # 行业类别进行数字化处理
    status_1 = [u'金融', u'企业服务', u'区块链', u'黄金', u'保险']
    status_2 = [u'汽车交通', u'交通运输', u'物流', u'养护']
    status_3 = [u'消费', u'旅游', u'文化娱乐', u'酒店', u'生活服务', u'食品饮料', u'电商', u'体育', u'社交',
                u'消费生活', u'文娱传媒', u'会员', u'商业地产', u'乳制品', u'服饰', u'VRAR', u'乐器', u'VR·AR', u'视频']
    status_4 = [u'医疗', u'教育', u'环保', u'公用事业', u'医疗健康', u'中药研发' ]
    status_5 = [u'传统行业', u'能源矿产', u'钢铁', u'生产制造', u'工具', u'轮胎', u'材料', u'能源矿产', u'水泥',
                u'化工', u'污水处理', u'开采', u'水处理', u'锅炉', u'太阳能光伏', u'压缩机', u'零配件', u'燃气', u'石油',
                u'液压', u'供水', u'工程机械', u'电机', u'数控机床', u'自动化', u'纤维', u'能源开采', u'园林绿化', u'产品研发',
                u'阀门', u'pvc', u'冷链', u'制冷', u'纺织', u'机电', u'风机', u'变压器', u'压缩机', u'混凝土', u'开采', u'面料',
                u'电气', u'印刷', u'橡胶',u'机床']
    status_6 = [u'建筑施工', u'房地产', u'工程施工', u'地产建筑', u'建筑材料', u'房产家居', u'建筑装饰']
    status_7 = [u'智能硬件', u'人工智能', u'智能终端', u'航空', u'先进制造', u'硬件', u'无人机', u'光电', u'大数据',
                u'工业安全监控', u'火箭', u'物联网', u'智能淋浴', u'智慧城市', u'机器人', u'生态系统', u'智慧办公', u'云服务',
                u'激光', u'核电', u'数字视频']
    status_8 = [u'农业', u'农药', u'种子', u'兽药', u'农机研发', u'饲料']
    status_no = ['Unknown', 'Others', u'未知轮次']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8, status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, 8, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)

    return



def round(file_name, column_name):  # 行业类别进行数字化处理
    status_1 = [u'未融资']
    status_2 = [u'种子轮']
    status_3 = [u'天使轮']
    status_4 = [u'Pre-A轮']
    status_5 = [u'A轮']
    status_6 = [u'A+轮']
    status_7 = [u'Pre-B轮']
    status_8 = [u'B轮']
    status_9 = [u'B+轮']
    status_10 = [u'C轮']
    status_11 = [u'C+轮']
    status_12 = [u'D轮']
    status_13 = [u'E轮']
    status_14 = [u'E轮及以后']
    status_15 = [u'F轮']
    status_16 = [u'ICO']
    status_17 = [u'Pre-IPO']
    status_18 = [u'IPO']
    status_19 = [u'IPO后']
    status_20 = [u'上市']
    status_21 = [u'新三板']
    status_22 = [u'新三板定增']
    status_23 = [u'新四板']
    status_24 = [u'股权转让']
    status_25 = [u'债权融资']
    status_26 = [u'并购']
    status_27 = [u'战略合并']
    status_28 = [u'扶持基金']
    status_29 = [u'战略投资']
    status_30 = [u'被收购']
    status_31 = [u'后期阶段']
    status_32 = [u'私有化']
    status_33 = [u'众筹']
    status_34 = [u'主板定向增发']
    status_no = ['Unknown', u'未知轮次']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8, status_9, status_10,
                   status_11,status_12, status_13, status_14, status_15, status_16, status_17, status_18, status_19,
                   status_20, status_21, status_22, status_23, status_24, status_25, status_26, status_27, status_28,
                   status_29, status_30, status_31, status_32, status_33, status_34, status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                    28, 29, 30, 31, 32, 33, 34, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)

    return


def status(file_name, column_name):  # 行业类别进行数字化处理
    status_1 = [u'停止更新']
    status_2 = [u'已关闭']
    status_3 = [u'融资中']
    status_4 = [u'运营中']
    status_no = ['Unknown', u'未知轮次']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_no]
    status_after = [1, 2, 3, 4, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)

    return



def address(file_name, column_name, empty_mask='Unknown', others_mask='Others'):  # 行业类别进行数字化处理
    status_1 = [u'北京', u'上海', u'广州', u'深圳']
    status_2 = [u'成都', u'杭州', u'南京', u'武汉', u'天津', u'西安', u'重庆', u'青岛', u'沈阳', u'长沙', u'大连',
                u'厦门', u'无锡', u'福州', u'济南']
    status_3 = ['Others']
    status_no = ['Unknown']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_no]
    status_after = [1, 2, 3, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)

    return




# def empty_value_handle_basic_info():
#     """
#     empty_value handle for table 竞品.
#     :return:
#     """
#     empty_check_list = [u'竞品的标签',
#                         u'竞品轮次',
#                         u'竞品运营状态',
#                         u'竞品成立时间']
#     dcu.drop_rows_too_many_empty(u'竞品.xlsx', columns=empty_check_list, thresh=3)
#     # panaly.list_category_columns_values([u'竞品'], u'竞品_empty_handled',
#     #                                     file_url=clean_data_temp_file_url)
#     return


def clean_competing_products():
    file_name = u'竞品'
    dcu.merge_status(file_name, u'竞品的行业'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'竞品详细地址'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'竞品运营状态'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'竞品成立时间'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'竞品轮次'.encode('utf-8'), [], [], empty_mask='Unknown')

    dcu.extract_keyword(file_name, u'竞品详细地址'.encode('utf-8'), [u'北京', u'上海', u'广州', u'深圳', u'成都',
                                                               u'杭州', u'南京', u'武汉', u'天津', u'西安', u'重庆',
                                                               u'青岛', u'沈阳', u'长沙', u'大连',u'厦门', u'无锡',
                                                               u'福州', u'济南'], empty_mask='Unknown', others_mask='Others')

    dcu.extract_keyword(file_name, u'竞品的标签'.encode('utf-8'), [u'金融', u'汽车交通', u'旅游', u'企业服务', u'传统行业',
                                                              u'能源矿产', u'生活服务', u'交通运输', u'建筑施工', u'物流',
                                                              u'房地产', u'钢铁', u'智能硬件', u'农业', u'医疗', u'文化娱乐',
                                                              u'人工智能', u'工程施工', u'酒店', u'智能终端', u'地产建筑',
                                                              u'食品饮料', u'消费', u'电商', u'生产制造', u'教育', u'航空',
                                                              u'先进制造', u'硬件', u'体育', u'社交', u'建筑材料', u'环保',
                                                              u'房产家居', u'工具', u'轮胎', u'农药', u'消费生活', u'材料',
                                                              u'能源矿产', u'水泥', u'化工', u'种子', u'无人机', u'光电',
                                                              u'公用事业', u'文娱传媒', u'医疗健康', u'污水处理', u'未知轮次'
                                                                                                  u'大数据',
                                                              u'工业安全监控'u'会员', u'开采', u'水处理', u'兽药',
                                                              u'锅炉', u'太阳能光伏', u'压缩机', u'火箭', u'农机研发', u'零配件',
                                                              u'区块链', u'燃气', u'商业地产', u'石油', u'液压', u'供水', u'工程机械',
                                                              u'乳制品', u'电机', u'机床', u'中药研发', u'黄金', u'自动化', u'能源开采'
                                                              u'纤维', u'保险', u'园林绿化', u'物联网', u'冷链', u'智能淋浴', u'智慧城市',
                                                              u'产品研发', u'机器人', u'服饰', u'阀门', u'养护', u'智慧办公',
                                                              u'pvc', u'制冷', u'生态系统', u'饲料', u'纺织', u'机电', u'风机',
                                                              u'云服务', u'激光', u'变压器', u'VRAR', u'压缩机', u'混凝土', u'核电',
                                                              u'开采', u'面料', u'电气', u'乐器', u'VR·AR', u'建筑装饰', u'印刷',
                                                              u'数字视频', u'橡胶', u'视频']
                        , empty_mask='Unknown', others_mask='Others')  # 对竞品标签的关键字进行处理，分析行业

    industry(file_name, u'竞品的标签'.encode('utf-8'))
    round(file_name, u'竞品轮次'.encode('utf-8'))
    status(file_name, u'竞品运营状态'.encode('utf-8'))
    address(file_name,u'竞品详细地址'.encode('utf-8'))

    return


