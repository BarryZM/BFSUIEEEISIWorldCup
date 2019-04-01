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
import pandas as pd


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

def time_rearranged(file_name, column_name):

    # 用split分开时间， 注意：之后数据分析所要用时间表头为0（数字格式）
    table = fu.read_file_to_df(clean_data_temp_file_url, file_name, sheet_name='Sheet')
    wr1 = pd.concat([table, table[column_name].str.split(r'-', expand=True)], axis=2, names=['year', 'month','day'])
    fu.write_file(wr1, clean_data_temp_file_url, file_name, ext='.xlsx',sheet_name='Sheet', index=False)

    dcu.drop_columns(file_name, 1 )
    return




def time_rearranged(file_name, column_name):
    df = fu.read_file_to_df(clean_data_temp_file_url, file_name, sheet_name='Sheet')  # 读取工作表
    df["year"], df["month"], df["day"] = df[column_name].str.split("-", n=2).str  # 分成三个表 n为劈开的次数
    df.drop(column_name, axis=1, inplace=True)  # 删除原有的列
    fu.write_file(df, clean_data_temp_file_url, file_name, ext='.xlsx', sheet_name='Sheet', index=False) # 保存

    # # 用split分开时间， 注意：之后数据分析所要用时间表头为0（数字格式）
    # table = fu.read_file_to_df(clean_data_temp_file_url, file_name, sheet_name='Sheet')
    # wr1 = pd.concat([table, table[column_name].str.split(r'-', expand=True)], axis=2, names=['year','month', 'day'])
    # fu.write_file(wr1, clean_data_temp_file_url, file_name, ext='.xlsx',sheet_name='Sheet', index=False)
    return

def money_kind(file_name, column_name):
    status_1 = [u'人民币']
    status_2 = [u'美元']
    status_no = ['Unknown', '-'] #错误的类别
    status_list = [status_1, status_2, status_no]
    status_after = [1, 2, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return





def industry_category(file_name, column_name):
    status_1 = ['A']
    status_2 = ['B']
    status_3 = ['C']
    status_4 = ['D']
    status_5 = ['E']
    status_6 = ['F']
    status_7 = ['G']
    status_8 = ['H']
    status_9 = ['I']
    status_10 = ['J']
    status_11 = ['G']
    status_12= ['K']
    status_13 = ['L']
    status_14 = ['M']
    status_15 = ['N']
    status_16 = ['O']
    status_17 = ['P']
    status_18 = ['Q']
    status_19 = ['R']
    status_no = ['Unknown'] #错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8, status_9, status_10,
                   status_11, status_12, status_13, status_14, status_15, status_16, status_17, status_18, status_19, status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def status_of_company(file_name, column_name):
    status_1 = [u'在营', u'存续', u'存续(在营、开业、在册)', u'开业', u'在营（开业）企业',
                u'存续（在营、开业、在册）']
    status_2 = [u'在业']
    status_3 = [u'迁出']
    status_no = ['Unknown']
    status_list = [status_1, status_2, status_3, status_no]
    status_after = [1, 2, 3, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def kind_of_company(file_name, column_name):
    status_1 = [u'外企']
    status_2 = [u'民营']
    status_no = ['Unknown'] #错误的类别
    status_list = [status_1, status_2, status_no]
    status_after = [1, 2, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def whether_on_stock_market(file_name, column_name):
    status_1 = ['N']
    status_2 = ['Y']
    status_no = ['Unknown'] #错误的类别
    status_list = [status_1, status_2, status_no]
    status_after = [1, 2, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def reason_log_out(file_name, column_name):
    status1 = [u'其他原因', u'决议解散', u'因公司合并或分立', u'宣告破产', u'章程规定的解散事由出现']
    status_no = ['-1']
    status_list = [status1, status_no]
    status_after = [1, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return





def clean_basic_info():
    file_name = u'工商基本信息表'

    dcu.drop_prefix_unit(file_name, u'行业小类（代码）'.encode('utf-8'), 'C')
    dcu.drop_prefix_unit(file_name, u'行业小类（代码）'.encode('utf-8'), 'J')

    dcu.merge_status(file_name, u'注册资本币种(正则)'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'经营状态'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'行业大类（代码）'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name,  u'行业小类（代码）'.encode('utf-8'), [], [], empty_mask='-1')
    dcu.merge_status(file_name, u'经营期限自'.encode('utf-8'), [], [], empty_mask='0000-00-00')
    dcu.merge_status(file_name, u'员工人数'.encode('utf-8'), [], [], empty_mask='-65535')
    dcu.merge_status(file_name, u'注销原因'.encode('utf-8'), [], [], empty_mask='-1')
    dcu.merge_status(file_name, u'注销时间'.encode('utf-8'), [], [], empty_mask='-1')

    time_rearranged(file_name, u'成立日期'.encode('utf-8'))

    dcu.drop_columns(file_name, u'城市代码'.encode('utf-8'))
    dcu.drop_columns(file_name, u'地区代码'.encode('utf-8'))
    dcu.drop_columns(file_name, u'登记机关区域代码'.encode('utf-8'))
    dcu.drop_columns(file_name, u'发照日期'.encode('utf-8'))
    dcu.drop_columns(file_name, u'经营期限自'.encode('utf-8'))
    dcu.drop_columns(file_name, u'经营期限至'.encode('utf-8'))

    money_kind(file_name,  u'注册资本币种(正则)'.encode('utf-8'))
    industry_category(file_name, u'行业大类（代码）'.encode('utf-8'))
    status_of_company(file_name, u'经营状态'.encode('utf-8'))
    kind_of_company(file_name, u'类型'.encode('utf-8'))
    whether_on_stock_market(file_name, u'是否上市'.encode('utf-8'))
    reason_log_out(file_name, u'注销原因'.encode('utf-8'))

    return


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


# {'Unknown':-1,'一般经济区域':1,'保税区':2,'保税港区、综合保税区':3,'保税物流园区':4,'经济技术开发全区':5,
#     '经济技术开发区':6,'经济特区':7,'高新技术产业开发区':8}.
def kind_of_range(file_name, column_name):
    status_1 = [u'一般经济区域']
    status_2 = [u'保税区']
    status_3 = [u'保税港区、综合保税区']
    status_4 = [u'保税物流园区']
    status_5 = [u'经济技术开发全区']
    status_6 = [u'经济技术开发区']
    status_7 = [u'经济特区']
    status_8 = [u'高新技术产业开发区']
    status_no = ['Unknown'] #错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8, status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, 8, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return

# {'临时注册企业':1,'保税仓库':2、'加工生产企业':3,'报关企业':4,'进出口收发货人':5,'进出口运输工具负责人':6 }.
def kind_of_tax_company(file_name, column_name):
    status_1 = [u'临时注册企业']
    status_2 = [u'保税仓库']
    status_3 = [u'加工生产企业']
    status_4 = [u'报关企业']
    status_5 = ['1', u'进出口收发货人']
    status_6 = [u'进出口运输工具负责人']
    status_no = ['Unknown'] #错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_no]
    status_after = [1, 2, 3, 4, 5, 6, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return

# 正常：1，注销：2
def log_out_custom(file_name, column_name):
    status_1 = [u'正常']
    status_2 = [u'注销']
    status_no = ['Unknown']  # 错误的类别
    status_list = [status_1, status_2, status_no]
    status_after = [1, 2, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return

# {超期未报告：1，未报告：2，超期报告：3，已报告：4, 不需要：5}
def status_of_annual_report(file_name, column_name):
    status_1 = [u'超期未报送']
    status_2 = [u'超期报送']
    status_3 = [u'未报送']
    status_4 = [u'已报送']
    status_5 = [u'不需要']
    status_no = ['Unknown']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_no]
    status_after = [1, 2, 3, 4, 5, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return

#  失信企业定位1，一般信用企业定为2，一般认证企业定为3，高级认证企业等位4.
def level_of_credit(file_name, column_name):
    status_1 = [u'失信企业']
    status_2 = [u'一般信用企业']
    status_3 = [u'一般认证企业']
    status_4 = [u'高级认证企业']
    status_no = ['Unknown']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_no]
    status_after = [1, 2, 3, 4, 5, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return




def clean_custom_credit():
    file_name = u'海关进出口信用'
    dcu.merge_status(file_name, u'经济区划'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'海关进出口信用', u'经营类别'.encode('utf-8'), [], [], empty_mask='Unknown')

    status_normal = [u'1']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个
    dcu.merge_status(u'海关进出口信用', u'信用等级'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'海关进出口信用', u'经济区划'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'海关进出口信用', u'海关注销标志'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(u'海关进出口信用', u'年报情况'.encode('utf-8'), [], [], empty_mask='Unknown')

    kind_of_range(file_name, u'经济区划'.encode('utf-8'))
    kind_of_tax_company(file_name, u'经营类别'.encode('utf-8'))
    log_out_custom(file_name,  u'海关注销标志'.encode('utf-8'))
    status_of_company(file_name, u'年报情况'.encode('utf-8'))
    level_of_credit(file_name, u'信用等级'.encode('utf-8'))

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


# {'中标':1,'公开招标':2,['其他','其它']:3,'单一':4,'变更':5,'合同':6,'废标':7,'成交':8, '招标':9,'拟建':10,'流标':11,
# '竞争性谈判':12,'竞价':13,'竞谈':14,'结果变更':15,'询价':16,'违规':17,'预告':18,'验收':19,'Unknown':-1}.
def status_of_announcement(file_name, column_name):
    status_1 = [u'中标']
    status_2 = [u'公开招标']
    status_3 = [u'其他', u'其它']
    status_4 = [u'单一']
    status_5 = [u'变更']
    status_6 = [u'合同']
    status_7 = [u'废标']
    status_8 = [u'成交']
    status_9 = [u'招标']
    status_10 = [u'拟建']
    status_11 = [u'流标']
    status_12 = [u'竞争性谈判']
    status_13 = [u'竞价']
    status_14 = [u'竞谈']
    status_15 = [u'结果变更']
    status_16 = [u'询价']
    status_17 = [u'违规']
    status_18 = [u'预告']
    status_19 = [u'验收']
    status_no = ['Unknown']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8, status_9, status_10,
                   status_11, status_12, status_13, status_14, status_15, status_16, status_17, status_18, status_19, status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def province(file_name, column_name):
    status_1 = [u'北京']
    status_2 = [u'天津']
    status_3 = [u'河北']
    status_4 = [u'山西']
    status_5 = [u'内蒙古']
    status_6 = [u'辽宁']
    status_7 = [u'吉林']
    status_8 = [u'黑龙江']
    status_9 = [u'上海']
    status_10 = [u'江苏', u'南京']
    status_11 = [u'浙江']
    status_12 = [u'安徽']
    status_13 = [u'福建']
    status_14 = [u'江西']
    status_15 = [u'山东']
    status_16 = [u'河南']
    status_17 = [u'湖北']
    status_18 = [u'湖南']
    status_19 = [u'广东']
    status_20 = [u'广西']
    status_21 = [u'海南']
    status_22 = [u'重庆']
    status_23 = [u'四川']
    status_24 = [u'贵州']
    status_25 = [u'云南']
    status_26 = [u'西藏']
    status_27 = [u'陕西']
    status_28 = [u'甘肃']
    status_29 = [u'青海']
    status_30 = [u'宁夏']
    status_31 = [u'新疆', u'兵团']
    status_32 = [u'台湾']
    status_33 = [u'香港']
    status_34 = [u'澳门']
    status_no = ['Unknown']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8, status_9, status_10,
                   status_11, status_12, status_13, status_14, status_15, status_16, status_17, status_18, status_19,
                   status_20,  status_21, status_22, status_23, status_24, status_25, status_26, status_27, status_28,
                   status_29, status_30,  status_31, status_32, status_33, status_34, status_no]
    status_after = [11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 51, 52, 53, 54,
                    61, 62, 63, 64, 65, 71, 81, 82, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def bidding_or_tendering(file_name, column_name):
    status_1 = [u'中标']
    status_2 = [u'招标']
    status_no = ['Unknown']  # 错误的类别
    status_list = [status_1, status_2,  status_no]
    status_after = [1, 2, 3, 4, 5, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return



def clean_tender():
    file_name = u'招投标'
    dcu.merge_status(file_name, u'公告类型'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'中标或招标'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'省份'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'发布时间'.encode('utf-8'), ['1970-01-01'], ['Unknown'], empty_mask='Unknown')


    status_of_announcement(file_name, u'公告类型'.encode('utf-8'))
    bidding_or_tendering(file_name, u'中标或招标'.encode('utf-8'))
    province(file_name, u'省份'.encode('utf-8'))
    time_rearranged(file_name, u'发布时间'.encode('utf-8'))
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
# {'C':1, 'CC':2, 'B':3, 'AA-':4, 'AA:5,'AA+':6,'AAA':7,'Unknown':-1}
def ranking_of_bond(file_name, column_name):
    status_1 = ['C']
    status_2 = ['CC']
    status_3 = ['B']
    status_4 = ['AA-']
    status_5 = ['AA']
    status_6 = ['AA+']
    status_7 = ['AAA']
    status_no = ['Unknown'] #错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


# {'中央企业债':1,'企业债券':2,'公司'、企业债':3,'地方企业债':4,'沪企债':5,'深企债':6,'银行间企债':7}.
def kind_of_bond(file_name, column_name):
    status_1 = [u'中央企业债']
    status_2 = [u'企业债券']
    status_3 = [u'公司、企业债']
    status_4 = [u'地方企业债']
    status_5 = [u'沪企债']
    status_6 = [u'深企债']
    status_7 = [u'银行间企债']
    status_no = ['Unknown', '-'] #错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return

# {'-':-1,'A':1, 'AA-':2, 'AA':3,'AA+':4,'AAA':5,'Unknown':-1}
def ranking_of_co(file_name, column_name):
    status_1 = ['A']
    status_2 = ['AA-']
    status_3 = ['AA']
    status_4 = ['AA+']
    status_5 = ['AAA']
    status_no = ['Unknown','-'] #错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_no]
    status_after = [1, 2, 3, 4, 5, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return

# {'到期一次还本付息':1,'按季付息':2, '半年付息':3, '按年付息':4,'附息式固定利率':5,'附息式浮动利率':6}
def interest_pay(file_name, column_name):
    status_1 = [u'到期一次还本付息']
    status_2 = [u'按季付息']
    status_3 = [u'半年付息']
    status_4 = [u'按年付息']
    status_5 = [u'附息式固定利率']
    status_6 = [u'附息式浮动利率']
    status_no = ['Unknown', '-'] #错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_no]
    status_after = [1, 2, 3, 4, 5, 6, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return



def clean_bond():
    file_name = u'债券信息'
    dcu.merge_status(file_name, u'债券信用评级'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'付息日期'.encode('utf-8'), [], [], empty_mask='0000-00-00')
    dcu.merge_status(file_name, u'兑付日期'.encode('utf-8'), [], [], empty_mask='0000-00-00')
    dcu.merge_status(file_name, u'主体信用评级'.encode('utf-8'), [], [], empty_mask='Unknown')  # 空值改为Unknown
    dcu.merge_status(file_name, u'债券品种'.encode('utf-8'),[], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'付息方式'.encode('utf-8'), [], [], empty_mask='Unknown')

    dcu.drop_unit(file_name, u'债券期限'.encode('utf-8'), [u'年'], empty_mask='Unknown')

    dcu.drop_columns(file_name, u'实际发行总额（亿元）'.encode('utf-8'))
    dcu.drop_columns(file_name, u'币种'.encode('utf-8'))
    dcu.drop_columns(file_name, u'流通场所'.encode('utf-8'))

    wr1 = fu.read_file_to_df(clean_data_temp_file_url,file_name,
                             sheet_name='Sheet')
    wr1 = wr1.fillna({u'纳税人资格'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引
    fu.write_file(wr1, clean_data_temp_file_url, file_name, ext='.xlsx',
                  sheet_name='Sheet', index=False)


    # wr1 = fu.read_file_to_df(clean_data_temp_file_url, file_name,
    #                          sheet_name='Sheet')
    # wr1 = wr1.fillna({u'实际发行总额（亿元）'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引
    # fu.write_file(wr1, clean_data_temp_file_url, file_name, ext='.xlsx',
    #               sheet_name='Sheet', index=False)


    wr1 = fu.read_file_to_df(clean_data_temp_file_url, file_name,
                             sheet_name='Sheet')
    wr1 = wr1.fillna({u'票面利率（%）'.encode('utf-8'): 'unknown'})  # 对空值进行处理以进行索引
    fu.write_file(wr1, clean_data_temp_file_url, file_name, ext='.xlsx',
                  sheet_name='Sheet', index=False)


    dcu.drop_columns(file_name, u'币种'.encode('utf-8'))
    dcu.drop_columns(file_name, u'流通场所'.encode('utf-8'))


    ranking_of_bond(file_name, u'债券信用评级'.encode('utf-8'))
    kind_of_bond(file_name, u'债券品种'.encode('utf-8'))
    ranking_of_co(file_name, u'主体信用评级'.encode('utf-8'))
    interest_pay(file_name, u'付息方式'.encode('utf-8'))


    time_rearranged(file_name, u'发行日期'.encode('utf-8'))
    time_rearranged(file_name, u'兑付日期'.encode('utf-8'))


    # status_normal = [u'']  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = ['Unknown']  # 改成这个
    # dcu.merge_status(u'债券信息', u'实际发行总额（亿元）'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')  # 空值改为Unknown

    # status_normal = [ ]  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = ['Unknown']  # 改成这个
    # dcu.merge_status(u'债券信息', u'票面利率（%）'.encode('utf-8'), status_list, status_after, empty_mask='Unknown')  # 空值改为Unknown



    # status_normal = []  # 搜索满足这个条件的
    # status_list = [status_normal]
    # status_after = []  # 改成这个


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

# { '天使轮': 1, '种子轮': 2, 'Pre-A轮': 3, 'A轮': 4, 'A+轮': 5, 'B轮': 6, 'B+轮': 7, 'C轮': 8, 'C+轮': 9,  'D轮': 10,
# 'E轮': 11, 'E轮及以后': 12, 'F轮': 13, 'Pre-IPO': 14, 'IPO': 15, 'IPO后': 16, '上市': 17, '上市后': 18, '后期阶段': 21,
# '主板定向增发': 19, '债权融资': 20,  '并购': 22, '战略合并': 23, '战略投资': 24, '新三板': 25, '新三板定增': 26, '私有化': 27,
# '股权转让': 28, '被收购': 29}
def round(file_name, column_name):  # 行业类别进行数字化处理
    status_1 = [u'种子轮']
    status_2 = [u'天使轮']
    status_3 = [u'Pre-A轮']
    status_4 = [u'A轮']
    status_5 = [u'A+轮']
    status_6 = [u'B轮']
    status_7 = [u'B+轮']
    status_8 = [u'C轮']
    status_9 = [u'C+轮']
    status_10 = [u'D轮']
    status_11 = [u'E轮']
    status_12 = [u'E轮及以后']
    status_13 = [u'F轮']
    status_14 = [u'Pre-IPO']
    status_15 = [u'IPO']
    status_16 = [u'IPO后']
    status_17 = [u'上市']
    status_18 = [u'上市后']
    status_19 = [u'后期阶段']
    status_20 = [u'主板定向增发']
    status_21 = [u'债权融资']
    status_22 = [u'并购']
    status_23 = [u'战略合并']
    status_24 = [u'战略投资']
    status_25 = [u'新三板']
    status_26 = [u'新三板定增']
    status_27 = [u'私有化']
    status_28 = [u'股权转让']
    status_29 = [u'被收购']

    status_no = ['Unknown', u'未知轮次']  # 错误的类别
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8, status_9, status_10,
                   status_11,status_12, status_13, status_14, status_15, status_16, status_17, status_18, status_19,
                   status_20, status_21, status_22, status_23, status_24, status_25, status_26, status_27, status_28,
                   status_29,  status_no]
    status_after = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                    28, 29,  -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)




def clean_financing():
    file_name = u'融资信息'
    dcu.merge_status(file_name, u'融资日期'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'轮次'.encode('utf-8'), [], [], empty_mask='Unknown')

    round(file_name, u'轮次'.encode('utf-8'))

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



