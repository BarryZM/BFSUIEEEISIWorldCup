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
import file_utils as fu
import primary_analysis as panaly
from file_directions import clean_data_temp_file_url
from files_category_info import category_basic_information


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_basic_information, u'基本信息类')
    return


#  TODO handle all the duplicate data in all tables listed in '基本信息类'


def duplicate_handle():
    for name in category_basic_information:
        dcu.merge_rows(name + '.xlsx')
        return


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_basic_information, u'基本信息类_dup_handled',
                                        file_url=clean_data_temp_file_url)
    return


"""
    Dirty value handle for table 工商基本信息表.xlsx.
    First we'll drop rows that empty value is too many.
    # ['发照日期','员工人数','地区代码','城市代码', '成立日期','是否上市',' 注册资本币种(正则)','注册资本（万元）','登记机关区域代码','省份代码',
    '类型','经营期限自','经营期限至','经营状态','行业大类（代码）','行业小类（代码）']
    # Once there are more than 1 empties in these 16 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    注册资本（万元）
    ------
    Empty percentage is 0%(0 out of 3000).
    All the information is good as there is no empty value here and all the values here are above 0 and with just numbers
    in it. So we can use it without any change.
    -----------------------------
    注册资本币种(正则)
    ------
    Empty percentage is 0%(0 out of 3000).
    2 status can be concluded in this part, they are [‘人民币’,‘美元’,'-']
    480 values are '-', and the '-' can be considered as 'unknown'. As it didn't account for a large scale, we can drop the unknown value.
    So we can map these total 2 status : {'人民币':0,'美元':1}.
    -----------------------------
    成立日期
    ------
    Empty percentage is 0%(0 out of 3000).
    All the information is good as there is no empty value here and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    经营状态
    ------
    Empty percentage is 0%(0 out of 3000).
    7 status this value has, they are ['在业','在营','存续','存续(在营、开业、在册)','存续(在营、开业、在册)','开业','迁出'].
    Cause there is no empty values here so we will not add another type about empty.
    According to the classification from the accounting, we can conclude ['在营','存续','存续(在营、开业、在册)','存续(在营、开业、在册)','开业']
    as one group of '存续', so we can map these total 7 status to 3: {'存续':0,'在业':1,'迁出':2}.
    -----------------------------
    -----------------------------
    行业大类（代码）
    ------
    Empty percentage is 0.03%(1 out of 3000).
    18 status this value has, they are ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R']
    Empty values can be concluded to 'Unknown'
    So we can map it with 19 status:
    {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'J':9,'K':10,'L':11,'M':12,'N':13,'O':14,'P':15,'Q':16,'R':17, 'Unknown':-1}.
    -----------------------------
    行业小类（代码）
    ------
    Empty percentage is 0.03%(1 out of 3000).
    82 status are in this column and most of the values are showed by the pure number. However, we can still find that
    there are two values aren't showed by the pure number. So we need to drop the character and change them to pure number
    Empty values can be concluded to 'Unknown'
    So we can finally map it with 80 status:
    -----------------------------
    类型
    ------
    Empty percentage is 0%(0 out of 3000).
    2 status can be concluded in this part, they are [‘外企’，‘民营’]
    All the information is good as there is no empty value here.  So we can map these total 2 status :
    {'外企':0,'民营':1}.
    -----------------------------
    省份代码
    ------
    Empty percentage is 0%(0 out of 3000).
    32 status can be concluded in this part. and all of the values are showed by the pure number
    All the information is good as there is no empty value here and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    城市代码
    ------
    Empty percentage is 0%(0 out of 3000).
    252 status can be concluded in this part. and all of the values are showed by the pure number
    All the information is good as there is no empty value here and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    地区代码
    ------
    Empty percentage is 0%(0 out of 3000).
    425 status can be concluded in this part. and all of the values are showed by the pure number
    All the information is good as there is no empty value here and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    是否上市
    ------
    Empty percentage is 0%(0 out of 3000).
    2 status can be concluded in this part, they are [‘N’，‘Y’]
    All the information is good as there is no empty value here.  So we can map these total 2 status : {'N':0,'Y':1}.
    -----------------------------
    经营期限自
    ------
    Empty percentage is 0.43%(13 out of 3000).  Empty values can be concluded to 'Unknown'
    Now all the information is good as there is no empty value here and there isn't any values that break the logic. So we
    can use it.
    -----------------------------
    经营期限至
    ------
    Empty percentage is 82.63%(2479 out of 3000).
    We consider each part as an independent status, for these empty value, we just add another status: 'Unknown'.
    -----------------------------
    登记机关区域代码
    ------
    Empty percentage is 0.27%(8 out of 3000).
    Empty values can be concluded to 'Unknown'
    Now 276 status can be concluded in this part. and all of the values are showed by the pure number
    All the information is good as there is no empty value here now and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    发照日期
    ------
    Empty percentage is 0.7%(21 out of 3000).
    Empty values can be concluded to 'Unknown'
    Now we consider each part as an independent status. and all of the values are showed by correct format of time.
    All the information is good as there is no empty value here now and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    员工人数
    ------
    Empty percentage is 0.47%(14 out of 3000).
    Empty values can be concluded to 'Unknown'
    Now we consider each part as an independent status. and all of the values are showed by pure number.
    All the information is good as there is no empty value here now and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    注销原因
    ------
    Empty percentage is 92.43%(2773 out of 3000).
    5 status can be concluded in this part, they are [‘其他原因’，‘决议解散’,'因公司合并或分立','宣告破产','章程规定的解散事由出现']
    As this column is important for the value of a company. So we just add another status for the empty value:'Unknown'.
    So we can map these total 6 status : {‘其他原因’:0，‘决议解散’:1,'因公司合并或分立':2,'宣告破产':3,'章程规定的解散事由出现':4,'Unknown':-1}.
    -----------------------------
    注销时间
    ------
    Empty percentage is 99.97%(2999 out of 3000).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    As this column is important for the value of a company. So we just add another status for the empty value:'Unknown'.
    -----------------------------
"""


# def empty_value_handle_basic_info():
#     empty_check_list = [u'发照日期',
#                         u'员工人数',
#                         u'地区代码',
#                         u'城市代码',
#                         u'成立日期',
#                         u'是否上市',
#                         u'注册资本币种(正则)',
#                         u'注册资本（万元）',
#                         u'登记机关区域代码',
#                         u'省份代码',
#                         u'类型',
#                         u'经营期限自',
#                         u'经营期限至',
#                         u'经营状态',
#                         u'行业大类（代码）',
#                         u'行业小类（代码）']
#     dcu.drop_rows_too_many_empty(u'工商基本信息表.xlsx', columns=empty_check_list, thresh = 2)
#     return


def clean_basic_info():
    status_normal = [u'-']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个
    dcu.merge_status(u'工商基本信息表', u'注册资本币种(正则)'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')

    status_normal = [u'在营', u'存续', u'存续(在营、开业、在册)', u'存续(在营、开业、在册)', u'开业']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = [u'存续']  # 改成这个
    dcu.merge_status(u'工商基本信息表', u'经营状态'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')

    dcu.drop_prefix_unit(u'工商基本信息表', u'行业小类（代码）'.encode('utf-8'), 'C')
    dcu.drop_prefix_unit(u'工商基本信息表', u'行业小类（代码）'.encode('utf-8'), 'J')

    dcu.merge_status(u'工商基本信息表', u'行业大类（代码）'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'工商基本信息表',  u'行业小类（代码）'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'工商基本信息表', u'经营期限自'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'工商基本信息表', u'经营期限至'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'工商基本信息表', u'登记机关区域代码'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'工商基本信息表', u'发照日期'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'工商基本信息表', u'员工人数'.encode('utf-8'), [], [], empty_mask='-65535')
    dcu.merge_status(u'工商基本信息表', u'注销原因'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'工商基本信息表', u'注销时间'.encode('utf-8'), [], [], empty_mask='Unknown')


"""
    Dirty value handle for table 海关进出口信用.xlsx.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    经济区划
    ------
    Empty percentage is 0.04%(1 out of 2605).
    8 status this value has, they are ['一般经济区域','保税区','保税港区'、'综合保税区','保税物流园区','经济技术开发全区',
    '经济技术开发区','经济特区','高新技术产业开发区'].
    Cause there is only 1 empty values here so we just drop the empty value and do not add another type about empty.
    So we can map these total 8 status: {'一般经济区域':0,'保税区':1,'保税港区、综合保税区':2,'保税物流园区':3,'经济技术开发全区':4,
    '经济技术开发区':5,'经济特区':6,'高新技术产业开发区':7}.
    -----------------------------
    经营类别
    ------
    Empty percentage is 0.08%(2 out of 2605).
    7 status this value has, they are ['1','临时注册企业','保税仓库'、'加工生产企业','报关企业','进出口收发货人','进出口运输工具负责人'].
    Cause there is only 2 empty values here so we just drop the empty value and do not add another type about empty.
    We look up the regulation about customs and find the code about different type of the enterprise.
    So we find that '1' is similar to '进出口收发货人', according to that, we can map these total 7 status to 6:
    {'临时注册企业':0,'保税仓库':1、'加工生产企业':2,'报关企业':3,'进出口收发货人':4,'进出口运输工具负责人':5 }.
    -----------------------------
    海关注销标志
    ------
    Empty percentage is 32.05%(835 out of 2605).
    2 status this value has, they are ['正常','注销'].
    As this column is important for the value of a company. So we just add another status for the empty value:'Unknown'.
    So we can map these total 3 status : {‘正常’:0，‘注销’:1,'Unknown':-1}.
    -----------------------------
    年报情况
    ------
    Empty percentage is 0%(0 out of 2605).
    5 status can be concluded in this part, they are [‘不需要’，‘已报送’,'未报送','超期报送','超期未报送']
    All the information is good as there is no empty value here.  So we can map these total 2 status :
    {‘不需要’:0，‘已报送’:1,'未报送':2,'超期报送':3,'超期未报送':4  }.
    -----------------------------
    信用等级
    ------
    Empty percentage is 48.06%(1252 out of 2605).
    4 status can be concluded in this part, they are ['一般信用企业','一般认证企业','失信企业','高级认证企业']
    As this column is important for the value of a company. So we just add another status for the empty value:'Unknown'.
    So we can map these total 5 status : {'一般信用企业','一般认证企业','失信企业','高级认证企业','Unknown':-1}.
    -----------------------------
"""


def empty_value_handle_custom_credit():
    """
    empty_value handle for table 基本信息.
    :return:
    """
    empty_check_list = [u'经济区划'.encode('utf-8'),
                        u'经营类别'.encode('utf-8'),
                        u'海关注销标志'.encode('utf-8'),
                        u'年报情况'.encode('utf-8'),
                        u'信用等级'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'海关进出口信用.xlsx', columns=empty_check_list, thresh=2)
    # panaly.list_category_columns_values([u'海关进出口信用'], u'海关进出口信用_empty_handled',
    #                                     file_url=clean_data_temp_file_url)


def clean_custom_credit():
    dcu.merge_status(u'海关进出口信用', u'经济区划'.encode('utf-8'), [], [], empty_mask='Unknown')
    # wr1 = fu.read_file_to_df(clean_data_temp_file_url, u'海关进出口信用.xlsx',
    #                          sheet_name='sheet')
    # wr1.fillna({u'经营类别': 'unknown'})  # 对空值进行处理以进行索引
    # wr1.ix[wr1[u'经营类别'].str.contains(u'1'), [u'出口状态备案状态']] = u'进出口收发货人'
    # fu.write_file(wr1, clean_data_temp_file_url, u'海关进出口信用', ext='.xlsx',
    #               sheet_name='Sheet', index=False)

    status_normal = [u'1']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = [u'进出口收发货人']  # 改成这个
    dcu.merge_status(u'海关进出口信用', u'经营类别'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')

    status_normal = [u'1']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个
    dcu.merge_status(u'海关进出口信用', u'信用等级'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')

    dcu.merge_status(u'海关进出口信用', u'经济区划'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'海关进出口信用', u'海关注销标志'.encode('utf-8'), [], [], empty_mask='Unknown')


    # wr1 = fu.read_file_to_df(clean_data_temp_file_url, u'海关进出口信用.xlsx',
    #                          sheet_name='sheet')
    # wr1 = wr1.fillna({u'信用等级': 'unknown'})  # 对空值进行处理以进行索引
    # fu.write_file(wr1, clean_data_temp_file_url, u'海关进出口信用', ext='.xlsx',
    #               sheet_name='Sheet', index=False)


    return


"""
    Dirty value handle for table 招投标.xlsx.
    First we'll drop rows that empty value is too many.
    # ['公告类型','发布时间','中标或招标','省份']
    # Once there are more than 1 empties in these 4 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
    to exploratory data analysis. 

    -----------------------------
    公告类型
    ------
    Empty percentage is 10.67%(8862 out of 83080).
    20 status can be concluded in this part, they are ['中标','公开招标','其他','其它','单一','变更','合同','废标','成交',
    '招标','拟建','流标','竞争性谈判','竞价','竞谈','结果变更','询价','违规','预告','验收']
    We just add another status for the empty value:'Unknown'.
    So we can map these total 21 status :{'中标':0,'公开招标':1,'其他':2,'其它':3,'单一':4,'变更':5,'合同':6,'废标':7,'成交':8,
    '招标':9,'拟建':10,'流标':11,'竞争性谈判':12,'竞价':13,'竞谈':14,'结果变更':15,'询价':16,'违规':17,'预告':18,'验收':19,'Unknown':-1}.
    -----------------------------
    中标或招标
    ------
    Empty percentage is 0%(0 out of 83080).
    2 status can be concluded in this part, they are ['中标','招标']
    All the information is good as there is no empty value here.  So we can map these total 2 status :
    {'中标'：0,'招标'：1}.
    -----------------------------
    省份
    ------
    Empty percentage is 0%(0 out of 83080).
    37 status can be concluded in this part, they are ['上海','云南','全国','兵团','内蒙古','北京','南京','台湾','吉林','四川',
    '天津','宁夏','安徽','山东','山西','广东','广西','新疆','江苏','江西','河北','河南','浙江','海南','湖北','湖南','澳门','甘肃',
    '福建','西藏','贵州','辽宁','重庆','陕西','青海','香港','黑龙江']
    Although there is no empty value here, some of the status should change due to the regulation.
    '兵团' should be concluded into '新疆', and '南京' should be concluded into '江苏'.
    Meanwhile, '全国' isn't the type of province, it seems similar to 'Unknown'. So we will use -1 to represent '全国'.
    So we can map these total 35 status : ['上海':0,'云南':1,'内蒙古':2,'北京':3,'台湾':4,'吉林':5,'四川':6,'天津':7,'宁夏':8,
    '安徽':9,'山东':10,'山西':11,'广东':12,'广西':13,'新疆':14,'江苏':15,'江西':16,'河北':17,'河南':18,'浙江':19,'海南':20,
    '湖北':21,'湖南':22,'澳门':23,'甘肃':24,'福建':25,'西藏':26,'贵州':27,'辽宁':28,'重庆':29,'陕西':30,'青海':31,'香港':32,
    '黑龙江':33,'全国':34]
    -----------------------------
    发布时间
    ------
    Empty percentage is 0%(0 out of 83080).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    But we can also find that the value '1970-01-01' is the default time of the computer system. So we need to drop them.
    After modifying that we can use it.
"""


def empty_value_handle_tenders():
    """
    empty_value handle for table 基本信息.
    :return:
    """
    empty_check_list = [u'公告类型'.encode('utf-8'),
                        u'发布时间'.encode('utf-8'),
                        u'中标或招标'.encode('utf-8'),
                        u'省份'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'招投标.xlsx', columns=empty_check_list, thresh=2)
    # panaly.list_category_columns_values([u'招投标'], u'招投标_empty_handled',
    #                                     file_url=clean_data_temp_file_url)
    return


def clean_tender():
    dcu.merge_status(u'招投标', u'公告类型'.encode('utf-8'), [], [], empty_mask='Unknown')


    status_normal = [u'兵团']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = [u'新疆']  # 改成这个
    dcu.merge_status(u'招投标', u'省份'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')

    status_normal = [u'南京']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = [u'江苏']  # 改成这个
    dcu.merge_status(u'招投标', u'省份'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')  # 空值改为Unknown

    return


"""
    Dirty value handle for table 债券信息.xlsx.
    First we'll drop rows that empty value is too many.
    # ['债券期限','债券品种','发行日期', '兑付日期','计划发行总额','票面利率','付息方式']
    # Once there are more than 3 empties in these 7 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
    to exploratory data analysis. 

    -----------------------------
    债券信用评级
    ------
    Empty percentage is 83.94%(1996 out of 2378).
    7 status can be concluded in this part, they are ['AA','AA+','AA-','AAA','B','C','CC']
    In China, not all companies have the rights to issue the bonds. So we just add another status for the empty value:'Unknown'.
    So we can map these total 8 status :{'AA:0,'AA+':1,'AA-':2,'AAA':3,'B':4,'C':5,'CC':6,'Unknown':-1}.
    -----------------------------
    债券期限
    ------
    Empty percentage is 3.62%(86 out of 2378). Some value end with '年' while some are pure number.
    Considering that all the unit in this value is '年', so we could drop the '年' and just remain the pure number.
    As the empty values account for a small scale, we could drop all the empty values.
    -----------------------------
    债券品种
    ------
    Empty percentage is 0%(0 out of 2378).
    7 status can be concluded in this part, they are ['中央企业债','企业债券','公司'、企业债','地方企业债','沪企债','深企债',
    '银行间企债']
    All the information is good as there is no empty value here. So we can map these total 7 status :
    {'中央企业债':1,'企业债券':2,'公司'、企业债':3,'地方企业债':4,'沪企债':5,'深企债':6,'银行间企债':7}.
    -----------------------------
    发行日期
    ------
    Empty percentage is 0%(0 out of 2378).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    So we can use them without change.
    -----------------------------
    付息日期
    ------
    Empty percentage is 15.31%(364 out of 2378).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    So we just add another status for the empty value:'Unknown' and representing with the number -1.
    -----------------------------
    兑付日期
    ------
    Empty percentage is 3.66%(87 out of 2378).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    So we just add another status for the empty value:'Unknown' and representing with the number -1.
    -----------------------------
    计划发行总额（亿元）
    ------
    Empty percentage is 0%(0 out of 2378).
    We consider each part as an independent status. and all of the values are showed by pure number.
    All the information is good as there is no empty value here now and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    实际发行总额（亿元）
    ------
    Empty percentage is 98.53%(2343 out of 2378).
    We consider each part as an independent status. and all of the values are showed by pure number.
    We just add another status for the empty value:'Unknown' and representing with the number -1.
    All the information is good as there is no empty value here now and there isn't any values that break the logic. So we
    can use it without change.
    -----------------------------
    币种
    ------
    Empty percentage is 0%(0 out of 2378).
    As there is just one status '人民币', so we can drop this column.
    -----------------------------
    流通场所
    ------
    Empty percentage is 99.24%(2360 out of 2378).
    6 status can be concluded in this part, they are ['null','上交所','其他'、'银行间债券市场','银行间债券市场 柜台',
    '银行间债券市场 深交所']
    As there are too many empty values and the column isn't important for the value of the company. So we can drop it.
    -----------------------------
    票面利率（%）
    ------
    Empty percentage is 0.17%(4 out of 2378).
    As the empty values account for a small scale, so we can drop them.
    Now we consider each part as an independent status. and all of the values are showed by pure number.
    All the information is good as there is no empty value here now and there isn't any values that break the logic. So we
    can use it without any change.
    -----------------------------
    主体信用评级
    ------
    Empty percentage is 84.10%(2000 out of 2378).
    6 status can be concluded in this part, they are ['-','A','AA','AA+','AA-','AAA']
    In China, not all companies have the rights to issue the bonds. So we just add another status for the empty value:
    'Unknown' and use -1 to represent it.
    And we can consider '-' is similar to 'Unknown'.
    So we can map these total 8 status :{'-':0,'A':1,'AA':2,'AA+':3,'AA-':4,'AAA':5,'Unknown':-1}.
    -----------------------------
    付息方式
    ------
    Empty percentage is 0%(0 out of 2378).
    6 status can be concluded in this part, they are ['到期一次还本付息','半年付息','按季付息','按年付息','附息式固定利率',
    '附息式浮动利率']
    All the information is good as there is no empty value here.  So we can map these total 2 status : {'到期一次还本付息':0,
    '半年付息':1,'按季付息':2,'按年付息':3,'附息式固定利率':4,'附息式浮动利率':5}.
    -----------------------------
"""


# def empty_value_handle_bond():
#
#
#     """
#     empty_value handle for table 基本信息.
#     :return:
#     """
#     empty_check_list = [u'债券期限'.encode('utf-8'),
#                         u'债券品种'.encode('utf-8'),
#                         u'发行日期'.encode('utf-8'),
#                         u'兑付日期'.encode('utf-8'),
#                         u'计划发行总额'.encode('utf-8'),
#                         u'票面利率'.encode('utf-8'),
#                         u'付息方式'.encode('utf-8')]
#     dcu.drop_rows_too_many_empty(u'债券信息.xlsx', columns=empty_check_list, thresh=2)
#     # panaly.list_category_columns_values([u'债券信息'], u'债券信息_empty_handled',
#     #                                     file_url=clean_data_temp_file_url)
#     return


def clean_bond():
    dcu.merge_status(u'债券信息', u'债券信用评级'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'债券信息', u'付息日期'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'债券信息', u'兑付日期'.encode('utf-8'), [], [], empty_mask='Unknown')

    dcu.drop_unit(u'债券信息', u'债券期限'.encode('utf-8'), [u'年'], empty_mask='Unknown')

    wr1 = fu.read_file_to_df(clean_data_temp_file_url, u'债券信息.xlsx',
                             sheet_name='Sheet')
    wr1 = wr1.fillna({u'纳税人资格'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引
    fu.write_file(wr1, clean_data_temp_file_url, u'债券信息', ext='.xlsx',
                  sheet_name='Sheet', index=False)

    dcu.drop_columns(u'债券信息', u'币种'.encode('utf-8'))
    dcu.drop_columns(u'债券信息', u'流通场所'.encode('utf-8'))

    wr1 = fu.read_file_to_df(clean_data_temp_file_url, u'债券信息.xlsx',
                             sheet_name='Sheet')
    wr1 = wr1.fillna({u'实际发行总额（亿元）'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引
    fu.write_file(wr1, clean_data_temp_file_url, u'债券信息', ext='.xlsx',
                  sheet_name='Sheet', index=False)

    # status_normal = [u'']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = ['Unknown']  # 改成这个
    # dcu.merge_status(u'债券信息', u'实际发行总额（亿元）'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')  # 空值改为Unknown

    # status_normal = [ ]  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = ['Unknown']  # 改成这个
    # dcu.merge_status(u'债券信息', u'票面利率（%）'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')  # 空值改为Unknown

    wr1 = fu.read_file_to_df(clean_data_temp_file_url, u'债券信息.xlsx',
                             sheet_name='Sheet')
    wr1 = wr1.fillna({u'票面利率（%）'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引
    fu.write_file(wr1, clean_data_temp_file_url, u'债券信息', ext='.xlsx',
                  sheet_name='Sheet', index=False)

    status_normal = [u'-']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个
    dcu.merge_status(u'债券信息', u'主体信用评级'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')  # 空值改为Unknown

    return


"""
    Dirty value handle for table 融资信息.xlsx.
    First we'll drop rows that empty value is too many.
    # ['融资日期','轮次','投资金额']
    # Once there are more than 1 empty in these 3 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    融资日期
    ------
    Empty percentage is 0.22%(10 out of 4468).
    We consider each part as an independent status. and all of the values are showed by correct format of time.
    As the empty values account for a small scale, we could drop all the empty values.
    -----------------------------
    轮次
    ------
    Empty percentage is 0%(0 out of 4468).
    29 status this value has, they are ['A+轮','A轮','B+轮','B轮','C+轮','C轮','D轮','E轮','E轮及以后','F轮','IPO','IPO后',
    'Pre-A轮','Pre-IPO','上市','上市后','主板定向增发','债权融资','后期阶段','天使轮','并购','战略合并','战略投资','新三板',
    '新三板定增','私有化','种子轮','股权转让','被收购']
    Since there is no empty value. So we can map it with 29 status:
    {'A+轮':0,'A轮':1,'B+轮':2,'B轮':3,'C+轮':4,'C轮':5,'D轮':6,'E轮':7,'E轮及以后':8,'F轮':9,'IPO':10,'IPO后':11,'Pre-A轮':12,
    'Pre-IPO':13,'上市':14,'上市后':15,'主板定向增发':16,'债权融资':17,'后期阶段':18,'天使轮':19,'并购':20,'战略合并':21,
    '战略投资':22,'新三板':23,'新三板定增':24,'私有化':25,'种子轮':26,'股权转让':27,'被收购':28}
    -----------------------------
    投资金额
    ------
    Empty percentage is 0.98%(44 out of 4468).
    Some values end with '万人民币' and some values end with '万美元' and '万港币'， while  Some values end only with '万'.
    But also there are lots of values valued '未披露'(3309) and a few valued '数......' without number.
    Now for empty value and value valued '未披露', we conclude them into 'unknown' and use -1 to represent them.
    For values end with '万美元' and '万港币', we use the exchange to calculate their value in RMB and drop the unit.
    For values end only with '万', we consider both of them as the value that counted in RMB.
    For values end with '万人民币', we just drop the unit and change them to pure number.
    -----------------------------
"""


def empty_value_handle_financing():
    """
    empty_value handle for table 基本信息.
    :return:
    """
    empty_check_list = [u'融资日期'.encode('utf-8'),
                        u'轮次'.encode('utf-8'),
                        u'投资金额'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'融资信息.xlsx', columns=empty_check_list, thresh=2)
    # panaly.list_category_columns_values([u'债券信息'], u'债券信息_empty_handled',
    #                                     file_url=clean_data_temp_file_url)
    return


def clean_financing():
    column_name = u'投资金额'.encode('utf-8')
    wr1 = fu.read_file_to_df(clean_data_temp_file_url, u'融资信息.xlsx',
                             sheet_name='Sheet')
    wr1.fillna({column_name: 'Unknown'})  # 对空值进行处理以进行索引

    for index in range(0, len(wr1)):
        content = wr1.at[index, column_name]
        if str(content).startswith(u'数'):
            str1 = 'Unknown'
            wr1.set_value(index, column_name, str1)
        elif str(content).startswith(u'未披露'):
            str1 = 'Unknown'
            wr1.set_value(index, column_name, str1)
    fu.write_file(wr1, clean_data_temp_file_url, u'融资信息', ext='.xlsx',
                  sheet_name='Sheet', index=False)

    for index in range(0, len(wr1)):
        content = wr1.at[index, column_name]
        if str(content).endswith(u'万美元'):
            # num = re.sub(u'万美元','', str(content))
            num = str(content).replace(u'万美元', u'')  # 去除万美元并乘以美元汇率，从而换算成人民币
            numb = float(num)
            numc = numb * (10 ** 4) * 6.72  # 3月24日美元汇率
            wr1.set_value(index, column_name, numc)

        elif str(content).endswith(u'万港币'):
            # num = re.sub(u'万港币','', str(content))
            num = str(content).replace(u'万港币', '')  # 去除万美元并乘以港币汇率，从而换算成人民币
            numb = float(num)
            numc = numb * (10 ** 4) * 0.856  # 3月24日港币汇率
            wr1.set_value(index, column_name, numc)

        elif str(content).endswith(u'万人民币'):
            num = str(content).replace(u'万人民币', '')  # 去除万人民币
            numb = float(num)
            numc = numb * (10 ** 4)
            wr1.set_value(index, column_name, numc)

        elif str(content).endswith(u'万'):
            num = str(content).replace(u'万', '')  # 去除万人民币
            numb = float(num)
            numc = numb * (10 ** 4)
            wr1.set_value(index, column_name, numc)
    fu.write_file(wr1, clean_data_temp_file_url, u'融资信息', ext='.xlsx',
                  sheet_name='Sheet', index=False)

    return



