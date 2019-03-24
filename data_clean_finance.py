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


def duplicate_handle(): #删除重复行
    for name in category_finance_files:
        dcu.merge_rows(name + '.xlsx')


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_finance_files, u'财务信息类_dup_handled',
                                        file_url=clean_data_temp_file_url)
    return


def data_clean_finance_mgzb():
    """
            Dirty value handle for table 上市公司财务信息-每股指标.xlsx.
        # ['企业总评分','标题','日期','基本每股收益(元)', '扣非每股收益(元)','稀释每股收益(元)',
        '每股净资产(元)','每股公积金(元)','每股未分配利润(元)','每股经营现金流(元)']
        In this table, we turn all the '--' and nulls into 'NA'. Valid data are all in the form of double(float)

        -----------------------------
       企业总评分(企业编号)
        ------
        no change
        -----------------------------
        标题
        ------
        drop this column
        -----------------------------
        日期
        ------
        no change
        -----------------------------
        基本每股收益(元)
        ------
        turn '--' into 'NA'
        -----------------------------
        扣非每股收益(元)
        ------
        turn '--' into 'NA'
        -----------------------------
        稀释每股收益(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        -----------------------------
        每股净资产(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        -----------------------------
        每股公积金(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        -----------------------------
        每股未分配利润(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        -----------------------------
        每股经营现金流(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        -----------------------------
    """
    dcu.drop_columns(u'上市公司财务信息-每股指标', u'标题')

    # dcu.drop_columns(u'temp', u'c')
    # dcu.change_number('temp','a')

    status_normal = [u'--'] # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown'] # 改成这个
    dcu.merge_status(u'上市公司财务信息-每股指标', u'基本每股收益(元)', status_list, status_after)
    dcu.merge_status(u'上市公司财务信息-每股指标', u'扣非每股收益(元)', status_list, status_after)
    dcu.merge_status(u'上市公司财务信息-每股指标', u'稀释每股收益(元)', status_list, status_after, empty_mask='Unknown') # 空值改为Unknown
    dcu.merge_status(u'上市公司财务信息-每股指标', u'每股净资产(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市公司财务信息-每股指标', u'每股公积金(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市公司财务信息-每股指标', u'每股未分配利润(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市公司财务信息-每股指标', u'每股经营现金流(元)', status_list, status_after, empty_mask='Unknown')
    return


def data_clean_finance_cwfxzb():
    """
        Dirty value handle for table 上市信息财务信息-财务风险指标.xlsx.
        First we'll drop rows that empty value is too many.
        # ['企业总评分','标题','日期','资产负债率(%)','流动负债/总负债(%)','流动比率','速动比率']
        In this table, we turn all the '--' and nulls into 'NA'. Valid data are all in the form of double(float)


        -----------------------------
        标题
        ------
        drop this column
        -----------------------------
        日期
        ------
        no change
        -----------------------------
        资产负债率(%)
        ------
        turn '--%' into 'NA'
        -----------------------------
        流动负债/总负债(%)
        ------
        turn '--%' into 'NA'
        -----------------------------
        流动比率
        ------
        turn '--' into 'NA'
        -----------------------------
        速动比率
        ------
        turn '--' into 'NA'
        -----------------------------
    """
    dcu.drop_columns(u'上市信息财务信息-财务风险指标', u'标题')

    status_normal = [u'--', u'--%']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个

    dcu.merge_status(u'上市信息财务信息-财务风险指标', u'资产负债率(%)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-财务风险指标', u'流动负债/总负债(%)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-财务风险指标', u'流动比率', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-财务风险指标', u'速动比率', status_list, status_after, empty_mask='Unknown')

    # 去百分号
    # dcu.drop_unit(u'temp', u'a', unit_strs)
    unit_strs = [u'%']
    dcu.drop_unit(u'上市信息财务信息-财务风险指标', u'资产负债率(%)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息-财务风险指标', u'流动负债/总负债(%)', unit_strs)
    return

# import data_clean_finance
# dcu.merge_rows(u'上市信息财务信息-财务风险指标' + '.xlsx')
# data_clean_finance.data_clean_finance_cwfxzb()

def data_clean_finance_cznlzb():
    """
        Dirty value handle for table 上市信息财务信息-成长能力指标.xlsx.
    ['企业总评分','标题','日期','营业总收入(元)','毛利润(元)','归属净利润(元)',
    '扣非净利润(元)','营业总收入同比增长(元)','归属净利润同比增长(元)','扣非净利润同比增长(元)',
    '营业总收入滚动环比增长(元)','归属净利润滚动环比增长(元)','扣非净利润滚动环比增长(元)']
    后面六个变量单位是%

    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis. 

    -----------------------------
    标题
    ------
    drop this column
    -----------------------------
    日期
    ------
    no change
    -----------------------------
    营业总收入(元)
    ------
    turn '--' into 'NA'
    if end with u'万亿'
        drop u'万亿'
        *10^12
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8
    -----------------------------
    毛利润(元)
    ------
    turn '--' into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    归属净利润(元)
    ------
    turn '--' into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    扣非净利润(元)
    ------
    turn '--' into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    营业总收入同比增长(元)(%)
    ------
    turn '--%' into 'NA'

    -----------------------------
    归属净利润同比增长(元)(%)
    ------
    turn '--%' into 'NA'

    -----------------------------
    扣非净利润同比增长(元)(%)
    ------
    turn '--%' into 'NA'

    -----------------------------
    营业总收入滚动环比增长(元)(%)
    ------
    turn '--%' into 'NA'

    -----------------------------
    归属净利润滚动环比增长(元)(%)
    ------
    turn '--%' into 'NA'

    -----------------------------
    扣非净利润滚动环比增长(元)(%)
    ------
    turn '--%' into 'NA'

    -----------------------------
    dcu.change_number(u'temp',u'a',empty_mask='Unknown')
    """
    dcu.drop_columns(u'上市信息财务信息-成长能力指标', u'标题')

    status_normal = [u'--', u'--%']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个

    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'营业总收入(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'毛利润(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'归属净利润(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'扣非净利润(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'营业总收入同比增长(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'归属净利润同比增长(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'扣非净利润同比增长(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'营业总收入滚动环比增长(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'归属净利润滚动环比增长(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-成长能力指标', u'扣非净利润滚动环比增长(元)', status_list, status_after, empty_mask='Unknown')
    dcu.change_number(u'上市信息财务信息-成长能力指标', u'营业总收入(元)')
    dcu.change_number(u'上市信息财务信息-成长能力指标', u'毛利润(元)')
    dcu.change_number(u'上市信息财务信息-成长能力指标', u'归属净利润(元)')
    dcu.change_number(u'上市信息财务信息-成长能力指标', u'扣非净利润(元)')

    unit_strs = [u'%']
    dcu.drop_unit(u'上市信息财务信息-成长能力指标', u'营业总收入同比增长(元)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息-成长能力指标', u'归属净利润同比增长(元)',  unit_strs)
    dcu.drop_unit(u'上市信息财务信息-成长能力指标', u'扣非净利润同比增长(元)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息-成长能力指标', u'营业总收入滚动环比增长(元)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息-成长能力指标', u'归属净利润滚动环比增长(元)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息-成长能力指标', u'扣非净利润滚动环比增长(元)', unit_strs)

    return


def data_clean_finance_lrb():
    """
        Dirty value handle for table 上市信息财务信息-利润表.xlsx.
    First we'll drop rows that empty value is too many.
   ['企业总评分','标题','日期','营业收入(元)','营业成本(元)','销售费用(元)','财务费用(元)',
   '管理费用(元)','资产减值损失(元)','投资收益(元)','营业利润(元)','利润总额(元)','所得税(元)','归属母公司所有者净利润(元)']


    -----------------------------
    标题
    ------
    drop this column
    -----------------------------
    日期
    ------
    no change
    -----------------------------
    营业收入(元)
    ------
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    营业成本(元)
    ------
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    销售费用(元)
    ------
    turn '--' into 'NA'
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    财务费用(元)
    ------
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    管理费用(元)
    ------
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    资产减值损失(元)
    ------
    turn '--' into 'NA'
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    投资收益(元)
    ------
    turn '--' into 'NA'
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    营业利润(元)
    ------
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    利润总额(元)
    ------
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    所得税(元)
    ------
    turn '--' into 'NA'
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    归属母公司所有者净利润(元)
    ------
    turn null into 'NA'
    if end with u'万'
        drop u'万'
        *10^4
    if end with u'亿'
        drop u'亿'
        *10^8

    -----------------------------
    """
    dcu.drop_columns(u'上市信息财务信息-利润表', u'标题')

    status_normal = [u'--', u'--%']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个

    dcu.merge_status(u'上市信息财务信息-利润表', u'营业收入(元)',[], status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'营业成本(元)',[], status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'销售费用(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'财务费用(元)', [], status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'管理费用(元)', [], status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'资产减值损失(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'投资收益(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'营业利润(元)', [], status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'利润总额(元)', [], status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'所得税(元)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息-利润表', u'归属母公司所有者净利润(元)', status_list, status_after, empty_mask='Unknown')
    dcu.change_number(u'上市信息财务信息-利润表', u'营业收入(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'营业成本(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'销售费用(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'财务费用(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'管理费用(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'资产减值损失(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'投资收益(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'营业利润(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'利润总额(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'所得税(元)')
    dcu.change_number(u'上市信息财务信息-利润表', u'归属母公司所有者净利润(元)')

    return


def data_clean_finance_xjllb():
    """
        Dirty value handle for table 上市信息财务信息-现金流量表.xlsx.
    
    
        ['企业总评分','标题','日期','经营:销售商品、提供劳务收到的现金(元)','经营:收到的税费返还(元)','经营:收到其他与经营活动有关的现金(元)',
            '经营:经营活动现金流入小计(元)','经营:购买商品、接受劳务支付的现金(元)','经营:支付给职工以及为职工支付的现金(元)',
            '经营:支付的各项税费(元)','经营:支付其他与经营活动有关的现金(元)','经营:经营活动现金流出小计(元)','经营:经营活动产生的现金流量净额(元)',
            '投资:取得投资收益所收到的现金(元)','投资:处置固定资产、无形资产和其他长期资产收回的现金净额(元)','投资:投资活动现金流入小计(元)',
            '投资:购建固定资产、无形资产和其他长期资产支付的现金(元)','投资:投资支付的现金(元)','投资:投资活动现金流出小计(元)',
            '投资:投资活动产生的现金流量净额(元)','筹资:吸收投资收到的现金(元)','筹资:取得借款收到的现金(元)','筹资:筹资活动现金流入小计(元)',
            '筹资:偿还债务支付的现金(元)','筹资:分配股利、利润或偿付利息支付的现金(元)','筹资:筹资活动现金流出小计(元)','筹资活动产生的现金流量净额(元)']
    
    
    
        -----------------------------
        标题
        ------
        drop this column
        -----------------------------
        日期
        ------
        no change
        -----------------------------
        经营:销售商品、提供劳务收到的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:收到的税费返还(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:收到其他与经营活动有关的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:经营活动现金流入小计(元)
        ------
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:购买商品、接受劳务支付的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:支付给职工以及为职工支付的现金(元)
        ------
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:支付的各项税费(元)
        ------
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:支付其他与经营活动有关的现金(元)
        ------
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:经营活动现金流出小计(元)
        ------
        turn '--' into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        经营:经营活动产生的现金流量净额(元)
        ------
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        投资:取得投资收益所收到的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        投资:处置固定资产、无形资产和其他长期资产收回的现金净额(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        投资:投资活动现金流入小计(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        投资:购建固定资产、无形资产和其他长期资产支付的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        投资:投资支付的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        投资:投资活动现金流出小计(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        投资:投资活动产生的现金流量净额(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        筹资:吸收投资收到的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        筹资:取得借款收到的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        筹资:筹资活动现金流入小计(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        筹资:偿还债务支付的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        筹资:分配股利、利润或偿付利息支付的现金(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        筹资:筹资活动现金流出小计(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        筹资活动产生的现金流量净额(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
    """
    dcu.drop_columns(u'上市信息财务信息-现金流量表', u'标题')

    status_normal = [u'--']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个

    # 循环的写法
    # data_frame = file_utils.read_file_to_df(clean_data_temp_file_url,u'上市信息财务信息-现金流量表')
    #
    # for column in data_frame.columns:
    #     dcu.merge_status(u'上市信息财务信息-现金流量表', column, status_list, status_after)
    #     dcu.change_number(u'上市信息财务信息-现金流量表', column)

    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:销售商品、提供劳务收到的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:收到的税费返还(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:收到其他与经营活动有关的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:经营活动现金流入小计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:购买商品、接受劳务支付的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:支付给职工以及为职工支付的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:支付的各项税费(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:支付其他与经营活动有关的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:经营活动现金流出小计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'经营:经营活动产生的现金流量净额(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'投资:取得投资收益所收到的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'投资:处置固定资产、无形资产和其他长期资产收回的现金净额(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'投资:投资活动现金流入小计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'投资:购建固定资产、无形资产和其他长期资产支付的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'投资:投资支付的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'投资:投资活动现金流出小计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'投资:投资活动产生的现金流量净额(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'筹资:吸收投资收到的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'筹资:取得借款收到的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'筹资:筹资活动现金流入小计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'筹资:偿还债务支付的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'筹资:分配股利、利润或偿付利息支付的现金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'筹资:筹资活动现金流出小计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息-现金流量表', u'筹资活动产生的现金流量净额(元)', status_list, status_after)
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:销售商品、提供劳务收到的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:收到的税费返还(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:收到其他与经营活动有关的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:经营活动现金流入小计(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:购买商品、接受劳务支付的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:支付给职工以及为职工支付的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:支付的各项税费(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:支付其他与经营活动有关的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:经营活动现金流出小计(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'经营:经营活动产生的现金流量净额(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'投资:取得投资收益所收到的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'投资:处置固定资产、无形资产和其他长期资产收回的现金净额(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'投资:投资活动现金流入小计(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'投资:购建固定资产、无形资产和其他长期资产支付的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'投资:投资支付的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'投资:投资活动现金流出小计(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'投资:投资活动产生的现金流量净额(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'筹资:吸收投资收到的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'筹资:取得借款收到的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'筹资:筹资活动现金流入小计(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'筹资:偿还债务支付的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'筹资:分配股利、利润或偿付利息支付的现金(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'筹资:筹资活动现金流出小计(元)')
    dcu.change_number(u'上市信息财务信息-现金流量表', u'筹资活动产生的现金流量净额(元)')

    return


def data_clean_finance_ylnlzb():
    """
            Dirty value handle for table 上市信息财务信息盈利能力指标.xlsx.
    
        ['企业总评分','标题','日期','加权净资产收益率(%)','摊薄净资产收益率(%)','摊薄总资产收益率(%)','毛利率(%)','净利率(%)','实际税率(%)']

    
       -----------------------------
        标题
        ------
        drop this column
        -----------------------------
        日期
        ------
        no change
        -----------------------------
        加权净资产收益率(%)
        ------
        turn '--%' into 'NA'
        -----------------------------
        摊薄净资产收益率(%)
        ------
        turn '--%' into 'NA'
        -----------------------------
        摊薄总资产收益率(%)
        ------
        turn '--%' into 'NA'
        -----------------------------
        毛利率(%)
        ------
        turn '--%' into 'NA'
        if >100%
            turn into 'ERROR'
        -----------------------------
        净利率(%)
        ------
        turn '--%' into 'NA'
        if >100%
            turn into 'ERROR'
        -----------------------------
        实际税率(%)
        ------
        turn '--%' into 'NA'
        if >100%
            turn into 'ERROR'
        -----------------------------
    """
    dcu.drop_columns(u'上市信息财务信息盈利能力指标', u'标题')

    status_normal = [ u'--%']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个

    dcu.merge_status(u'上市信息财务信息盈利能力指标', u'加权净资产收益率(%)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息盈利能力指标', u'摊薄净资产收益率(%)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息盈利能力指标', u'摊薄总资产收益率(%)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息盈利能力指标', u'毛利率(%)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息盈利能力指标', u'净利率(%)', status_list, status_after, empty_mask='Unknown')
    dcu.merge_status(u'上市信息财务信息盈利能力指标', u'实际税率(%)', status_list, status_after, empty_mask='Unknown')

    unit_strs = [u'%']
    dcu.drop_unit(u'上市信息财务信息盈利能力指标', u'加权净资产收益率(%)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息盈利能力指标', u'摊薄净资产收益率(%)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息盈利能力指标', u'摊薄总资产收益率(%)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息盈利能力指标', u'毛利率(%)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息盈利能力指标', u'净利率(%)', unit_strs)
    dcu.drop_unit(u'上市信息财务信息盈利能力指标', u'实际税率(%)', unit_strs)

# 标记不合理的数据
#    dcu.mark_invalid_num_data(u'temp', u'a', '>', 100, error_mask='-65535')
    dcu.mark_invalid_num_data(u'上市信息财务信息盈利能力指标', u'毛利率(%)', '>', 100, error_mask='-65535')
    dcu.mark_invalid_num_data(u'上市信息财务信息盈利能力指标', u'净利率(%)', '>', 100, error_mask='-65535')
    dcu.mark_invalid_num_data(u'上市信息财务信息盈利能力指标', u'实际税率(%)', '>', 100, error_mask='-65535')

    return

def data_clean_finance_yynlzb():
    """
        Dirty value handle for table 上市信息财务信息运营能力指标.xlsx.
    
        ['企业总评分','标题','日期','总资产周转率(次)','应收账款周转天数(天)','存货周转天数(天)']'
    
    
        -----------------------------
        标题
        ------
        drop this column
        -----------------------------
        日期
        ------
        no change
        -----------------------------
        总资产周转率(次)
        ------
        turn null into 'NA'
        -----------------------------
        应收账款周转天数(天)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if <0
            turn into 'ERROR'
        -----------------------------
        存货周转天数(天)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if <0
            turn into 'ERROR'
        -----------------------------
        """
    dcu.drop_columns(u'上市信息财务信息运营能力指标', u'标题')

    status_normal = [u'--']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个

    # 第一行本来是数值型的，只能重新赋值成数值型的
    dcu.merge_status(u'上市信息财务信息运营能力指标', u'总资产周转率(次)', status_list, status_after, empty_mask='-65535')
    dcu.merge_status(u'上市信息财务信息运营能力指标', u'应收账款周转天数(天)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息运营能力指标', u'存货周转天数(天)', status_list, status_after)

    dcu.mark_invalid_num_data(u'上市信息财务信息运营能力指标', u'应收账款周转天数(天)', '<', 0, error_mask=-65535)
    dcu.mark_invalid_num_data(u'上市信息财务信息运营能力指标', u'存货周转天数(天)', '<', 0, error_mask=-65535)

    return


def data_clean_finance_zcfzb():
    """
        Dirty value handle for table 上市信息财务信息资产负债表.xlsx.
        First we'll drop rows that empty value is too many.
        # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
       ['企业总评分','标题','日期','资产:货币资金(元)','资产:应收账款(元)','资产:其它应收款(元)','资产:存货(元)','资产:流动资产合计(元)','资产:长期股权投资(元)','资产:累计折旧(元)','资产:固定资产(元)','资产:无形资产(元)','资产:资产总计(元)','负债:应付账款(元)','负债:预收账款(元)','负债:存货跌价准备(元)','负债:流动负债合计(元)','负债:长期负债合计(元)','负债:负债合计(元)','权益:实收资本(或股本)(元)','权益:资本公积金(元)','权益:盈余公积金(元)','权益:股东权益合计(元)','流动比率']
    
    
        -----------------------------
        标题
        ------
        drop this column
        -----------------------------
        日期
        ------
        no change
        -----------------------------
        资产:货币资金(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:应收账款(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:其它应收款(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:存货(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:流动资产合计(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:长期股权投资(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:累计折旧(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        资产:固定资产(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:无形资产(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        资产:资产总计(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        负债:应付账款(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        负债:预收账款(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        负债:存货跌价准备(元)
        ------
        turn '--' into 'NA'
        turn null into 'NA'
        if end with u'万'
            drop u'万'
            *10^4
        if end with u'亿'
            drop u'亿'
            *10^8
    
        -----------------------------
        负债:流动负债合计(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        负债:长期负债合计(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        负债:负债合计(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        权益:实收资本(或股本)(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        权益:资本公积金(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        权益:盈余公积金(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        权益:股东权益合计(元)
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        if end with u'亿' or u'亿'
            ='NA'
        -----------------------------
        流动比率
        ------
        turn null into 'NA'
        turn '--' into 'NA'
        -----------------------------
    """
    dcu.drop_columns(u'上市信息财务信息资产负债表', u'标题')

    status_normal = [u'--']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个

    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:货币资金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:应收账款(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:其它应收款(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:存货(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:流动资产合计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:长期股权投资(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:累计折旧(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:固定资产(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:无形资产(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'资产:资产总计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'负债:应付账款(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'负债:预收账款(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'负债:存货跌价准备(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'负债:流动负债合计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'负债:长期负债合计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'负债:负债合计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'权益:实收资本(或股本)(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'权益:资本公积金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'权益:盈余公积金(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'权益:股东权益合计(元)', status_list, status_after)
    dcu.merge_status(u'上市信息财务信息资产负债表', u'流动比率', status_list, status_after)

    dcu.change_number(u'上市信息财务信息资产负债表', u'资产:累计折旧(元)')
    dcu.change_number(u'上市信息财务信息资产负债表', u'负债:存货跌价准备(元)')

    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:货币资金(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:应收账款(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:其它应收款(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:存货(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:流动资产合计(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:长期股权投资(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:固定资产(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:无形资产(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'资产:资产总计(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'负债:应付账款(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'负债:预收账款(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'负债:流动负债合计(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'负债:长期负债合计(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'负债:负债合计(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'权益:实收资本(或股本)(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'权益:资本公积金(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'权益:盈余公积金(元)')
    dcu.merge_number_with_c(u'上市信息财务信息资产负债表', u'权益:股东权益合计(元)')

    return


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







