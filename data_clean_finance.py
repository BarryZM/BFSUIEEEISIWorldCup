# *- coding:utf-8 -*-

"""
 module for annual reports data clean.
 including:
上市公司财务信息-每股指标
上市信息财务信息-财务风险指标
上市信息财务信息-成长能力指标
上市信息财务信息-利润表
上市信息财务信息-现金流量表
上市信息财务信息盈利能力指标
上市信息财务信息运营能力指标
上市信息财务信息资产负债表
 Empty values are mostly replaced by -1.
"""

import data_clean_utils as dcu
import primary_analysis as panaly
from files_category_info import category_finance_files
from file_directions import clean_data_temp_file_url
import file_utils


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_finance_files, u'财务信息类') # 输入，输出，描述性统计



def duplicate_handle(): #该类别下所有的表都合并
    for name in category_finance_files:
        dcu.merge_rows(name + '.xlsx')


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_finance_files, u'财务信息类_dup_handled',
                                        file_url=clean_data_temp_file_url)


"""
    Dirty value handle for table 年报-企业基本信息.
    First we'll drop rows that empty value is too many.
    ['企业经营状态','从业人数','是否有网站或网点','企业是否有投资信息或购买其他公司股权',
        '有限责任公司本年度是否发生股东股权转','是否提供对外担保']
    Once there are more than 3 empties in these 6 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    注册资本
    ------
    Based on the primary analysis data, we can drop column 注册资本 which empty percentage is 88%
    -----------------------------
    企业经营状态
    ------
    Empty percentage is 1.5%(214 out of 14862).
    8 status this value has, they are ['停业','其他','存续','开业','开业/正常经营','歇业','正常开业','清算'].
    We just add another status for the empty value:'Unknown'.
    And based on the counts for every status, we simplify these status to ['正常经营','非正常经营','Unknown']
    ['开业','开业/正常经营','正常开业'] belongs to '正常经营' and ['停业','其他','存续','歇业','清算'] belongs to '非正常经营'.
    So we can map these total 9 status to three: {'正常经营':0,'非正常经营':1,'Unknown':-1}.
    -----------------------------
    从业人数
    ------
    Empty percentage is 1.5%(213 out of 14862), and some value end with '人' while some are pure number.
    But also there are lots of value valued '企业选择不公示'(11623) and a few valued '人' without number.
    For empty value, we replace with -1 indicating there's no value(be careful here, we don't trigger them as -1 people,
        -1 here works as a status). Those end with '人', we simply drop '人'. Those valued '企业选择不公示',
        we replace it as number 0 which also works as a status, there's 8 '0人's in the original value but
        shouldn't matter.
    -----------------------------
    是否有网站或网点
    ------
    Empty percentage is 1.5%(213 out of 14862).
    There are 4 status here:['否','无','是','有'], and ['否','无'] should belong to 'No', ['是','有'] belong to 'Yes'.
    Empty value will be replaced with
    -----------------------------
    企业是否有投资信息或购买其他公司股权
    ------

    -----------------------------
    有限责任公司本年度是否发生股东股权转
    ------

    -----------------------------
    是否提供对外担保
    ------

    -----------------------------
    发布日期
    ------

    -----------------------------
    年报年份


    -----------------------------
    :return:
"""
"""
    Dirty value handle for table 年报-企业资产状况信息.
    First we'll drop rows that empty value is too many.
    ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    主营业务收入
    ------

    -----------------------------
    净利润
    ------

    -----------------------------
    利润总额
    ------

    -----------------------------
    实际员工数量
    ------

    -----------------------------
    年报年份
    ------

    -----------------------------
    所有者权益合计
    ------

    -----------------------------
    纳税总额
    ------

    -----------------------------
    营业总收入
    ------

    -----------------------------
    负债总额
    ------

    -----------------------------
    资产总额
    ------

    -----------------------------
    
    :return:
"""
"""
    Dirty value handle for table 年报-对外投资信息.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 
    
    -----------------------------
    年报年份
    ------

    -----------------------------
    投资占比
    ------

    -----------------------------
    投资金额
    ------

    -----------------------------
    
    :return
"""
"""
    Dirty value handle for table 年报-的对外提供保证担保信息.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    主债权数额
    ------

    -----------------------------
    主债权种类
    ------

    -----------------------------
    保证担保的范围
    ------

    -----------------------------
    保证的方式
    ------

    -----------------------------
    保证的期间
    ------

    -----------------------------
    履行债务的期限
    ------

    -----------------------------
    年报年份
    ------

    -----------------------------

    :return
"""
"""
    Dirty value handle for table 年报-社保信息.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    单位参加城镇职工基本养老保险累计欠缴金额
    ------

    -----------------------------
    单位参加城镇职工基本养老保险缴费基数
    ------

    -----------------------------
    单位参加失业保险累计欠缴金额
    ------

    -----------------------------
    单位参加失业保险缴费基数
    ------

    -----------------------------
    单位参加工伤保险累计欠缴金额
    ------

    -----------------------------
    单位参加工伤保险缴费基数
    ------

    -----------------------------
    单位参加生育保险累计欠缴金额
    ------

    -----------------------------
    单位参加生育保险缴费基数
    ------

    -----------------------------
    单位参加职工基本医疗保险累计欠缴金额
    ------

    -----------------------------
    单位参加职工基本医疗保险缴费基数
    ------

    -----------------------------
    参加城镇职工基本养老保险本期实际缴费金额
    ------

    -----------------------------
    参加失业保险本期实际缴费金额
    ------

    -----------------------------
    参加工伤保险本期实际缴费金额
    ------

    -----------------------------
    参加生育保险本期实际缴费金额
    ------

    -----------------------------
    参加职工基本医疗保险本期实际缴费金额
    ------

    -----------------------------
    城镇职工基本养老保险人数
    ------

    -----------------------------
    失业保险人数
    ------

    -----------------------------
    工伤保险人数
    ------

    -----------------------------
    年报年份
    ------

    -----------------------------
    生育保险人数
    ------

    -----------------------------
    职工基本医疗保险人数
    ------

    -----------------------------

    :return
"""
"""
    Dirty value handle for table 年报-的对外提供保证担保信息.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    主债权数额
    ------

    -----------------------------
    主债权种类
    ------

    -----------------------------
    保证担保的范围
    ------

    -----------------------------
    保证的方式
    ------

    -----------------------------
    保证的期间
    ------

    -----------------------------
    履行债务的期限
    ------

    -----------------------------
    年报年份
    ------

    -----------------------------

    :return
"""

def empty_value_handle_basic_info():
    """
    empty_value handle for table 年报-企业基本信息.
    :return:
    """
    empty_check_list = [u'企业经营状态'.encode('utf-8'),
                        u'从业人数'.encode('utf-8'),
                        u'是否有网站或网点'.encode('utf-8'),
                        u'企业是否有投资信息或购买其他公司股权'.encode('utf-8'),
                        u'有限责任公司本年度是否发生股东股权转'.encode('utf-8'),
                        u'是否提供对外担保'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-企业基本信息.xlsx', columns=empty_check_list, thresh=3)
    # panaly.list_category_columns_values([u'年报-企业基本信息'], u'年报-企业基本信息_empty_handled',
    #                                     file_url=clean_data_temp_file_url)
    return


def empty_value_handle_assets_info():
    """
    empty_value handle for table 年报-企业资产状况信息.
    :return:
    """
    empty_check_list = [u'主营业务收入'.encode('utf-8'),
                        u'净利润'.encode('utf-8'),
                        u'利润总额'.encode('utf-8'),
                        u'所有者权益合计'.encode('utf-8'),
                        u'纳税总额'.encode('utf-8'),
                        u'营业总收入'.encode('utf-8'),
                        u'负债总额'.encode('utf-8'),
                        u'资产总额'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-企业资产状况信息.xlsx', columns=empty_check_list, thresh=3)
    # panaly.list_category_columns_values([u'年报-企业资产状况信息'], u'年报-企业资产状况信息_empty_handled',
    #                                     file_url=clean_data_temp_file_url)
    return


def empty_value_handle_out_invest_info():
    """
    empty_value handle for table 年报-对外投资信息.
    Don't drop data in this table, just replace the empty with 0.
    :return:
    """

    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'年报-对外投资信息')
    df = df.fillna(0)
    file_utils.write_file(df, clean_data_temp_file_url, u'年报-对外投资信息')

    # panaly.list_category_columns_values([u'年报-对外投资信息'], u'年报-对外投资信息_empty_handled',
    #                                     file_url=clean_data_temp_file_url)
    return


def numeric_handle_basic_info():
    """
    numeric data for table 年报-企业基本信息.
    :return:
    """
