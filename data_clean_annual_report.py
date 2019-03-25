# *- coding:utf-8 -*-

"""
 module for annual reports data clean.
 including:
    年报-企业基本信息
    年报-企业资产状况信息
    年报-对外投资信息
    年报-的对外提供保证担保信息
    年报-社保信息
    年报-网站或网点信息
    年报-股东股权转让
    年报-股东（发起人）及出资信息

 Empty values are mostly replaced by -1.
"""

import data_clean_utils as dcu
import file_utils
import primary_analysis as panaly
from file_directions import clean_data_temp_file_url
from files_category_info import category_annual_report_files
import pandas


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_annual_report_files, u'年报类')


def duplicate_handle():
    for name in category_annual_report_files:
        if name == u'年报-对外投资信息':
            continue
        dcu.merge_rows(name + '.xlsx')


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_annual_report_files, u'年报类_dup_handled',
                                        file_url=clean_data_temp_file_url)


def empty_value_handle_basic_info():
    """
    empty_value handle for table 年报-企业基本信息.
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
    Empty percentage is 0%(1 out of 14862).
    8 status this value has, they are ['停业','其他','存续','开业','开业/正常经营','歇业','正常开业','清算'].
    We just add another status for the empty value:'Unknown'.
    And based on the counts for every status, we simplify these status to ['正常经营','非正常经营','Unknown']
    ['开业','开业/正常经营','正常开业'] belongs to '正常经营' and ['停业','其他','存续','歇业','清算'] belongs to '非正常经营'.
    So we can map these total 9 status to three: {'正常经营':0,'非正常经营':1,'Unknown':-1}.
    -----------------------------
    从业人数
    ------
    Empty percentage is 0%(0 out of 14862), and some value end with '人' while some are pure number.
    But also there are lots of value valued '企业选择不公示'(11623) and a few valued '人' without number.
    For empty value, we replace with -1 indicating there's no value(be careful here, we don't trigger them as -1 people,
        -1 here works as a status). Those end with '人', we simply drop '人'. Those valued '企业选择不公示',
        we replace it as number 0 which also works as a status, there's 8 '0人's in the original value but
        shouldn't matter.
    -----------------------------
    是否有网站或网点
    ------
    Empty percentage is 0%(0 out of 14862).
    There are 4 status here:['否','无','是','有'], and ['否','无'] should belong to 'No', ['是','有'] belong to 'Yes'.
    -----------------------------
    企业是否有投资信息或购买其他公司股权
    ------
    Empty percentage is 0.02%(3 out of 14862).
    There are 4 status here:['否','无','是','有'], and ['否','无'] should belong to 'No', ['是','有'] belong to 'Yes'.
    Empty value will be mapped to 'Unknown'.
    -----------------------------
    有限责任公司本年度是否发生股东股权转
    ------
    Empty percentage is 0.013%(2 out of 14862).
    There are 4 status here:['否','无','是','有'], and ['否','无'] should belong to 'No', ['是','有'] belong to 'Yes'.
    Empty value will be mapped to 'Unknown'.
    -----------------------------
    是否提供对外担保
    ------
    Empty percentage is 0.075%(11 out of 14862).
    There are 2 status here:['否','是'], we map them to ['No', 'Yes'].
    Empty value will be mapped to 'Unknown'.
    -----------------------------
    发布日期
    ------
    Empty percentage is 0%(0 out of 14862).
    And it's well formatted, so without any process on this column.

    -----------------------------
    年报年份
    ------
    Empty percentage is 0%(0 out of 14862).
    And it's well formatted, so without any process on this column.
    -----------------------------
    :return:
    """
    # EMPTY CHECK
    empty_check_list = [u'企业经营状态'.encode('utf-8'),
                        u'从业人数'.encode('utf-8'),
                        u'是否有网站或网点'.encode('utf-8'),
                        u'企业是否有投资信息或购买其他公司股权'.encode('utf-8'),
                        u'有限责任公司本年度是否发生股东股权转'.encode('utf-8'),
                        u'是否提供对外担保'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-企业基本信息.xlsx', columns=empty_check_list, thresh=3)

    # LIST OUT VALUES AFTER EMPTY ROWS HANDLED
    panaly.list_category_columns_values([u'年报-企业基本信息'], u'年报-企业基本信息_empty_handled',
                                        file_url=clean_data_temp_file_url)

    # COLUMNS HANDLE
    # 注册资本
    dcu.drop_columns(u'年报-企业基本信息', [u'注册资本'.encode('utf-8')])

    # 企业经营状态
    status_normal = [u'开业', u'开业/正常经营', u'正常开业']
    status_unnormal = [u'停业', u'其他', u'存续', u'歇业', u'清算']
    status_list = [status_normal, status_unnormal]
    status_after = [u'正常经营', u'非正常经营', u'Unknown']
    dcu.merge_status(u'年报-企业基本信息', u'企业经营状态'.encode('utf-8'), status_list, status_after)

    # 从业人数
    dcu.drop_unit(u'年报-企业基本信息', u'从业人数'.encode('utf-8'), [u'人', u' 人'],
                  empty_mask=-1)

    # 是否有网站或网点
    yn_status_n = [u'否', u'无']
    yn_status_y = [u'是', u'有']
    yn_status_list = [yn_status_n, yn_status_y]
    yn_status_after = ['No', 'Yes']

    dcu.merge_status(u'年报-企业基本信息', u'是否有网站或网点'.encode('utf-8'), yn_status_list, yn_status_after)

    # 企业是否有投资信息或购买其他公司股权
    dcu.merge_status(u'年报-企业基本信息', u'企业是否有投资信息或购买其他公司股权'.encode('utf-8'), yn_status_list, yn_status_after)

    # 有限责任公司本年度是否发生股东股权转
    dcu.merge_status(u'年报-企业基本信息', u'有限责任公司本年度是否发生股东股权转'.encode('utf-8'), yn_status_list, yn_status_after)

    # 是否提供对外担保
    dcu.merge_status(u'年报-企业基本信息', u'是否提供对外担保'.encode('utf-8'), yn_status_list, yn_status_after)

    # 发布日期

    # 年报年份

    return


def empty_value_handle_assets_info():
    """
    Dirty value handle for table 年报-企业资产状况信息.xlsx.
    First we'll drop rows that empty value is too many.
    ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    资产总额
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11064 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    所有者权益合计
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11235 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    营业总收入
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11344 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    利润总额
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11304 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    主营业务收入
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11529 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    主营业务
    ------
    This value is very complicated with 80% empty(11745 out of 14657). But we think it's somehow important.
    We extract some key words:[u'农', u'土地', u'电器', u'光纤', u'电器', u'化学', u'医疗', u'药', u'信息', u'钢', u'乳',
                u'互联网', u'电机', u'自动化', u'交通', u'汽车', u'投资', u'园区', u'房地产', u'有线', u'日用', u'服饰',
                u'矿', u'开采', u'国有', u'酒', u'银行', u'金融', u'证券', u'航空', u'航天', u'采掘', u'发电', u'工程',
                u'制造'](the sequence is ordered to match the first), Others are into 'Others'. Empty values are
    replaced with 'Unknown'.

    -----------------------------
    净利润
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11292 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    纳税总额
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11292 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    负债总额
    ------
    Empty percentage is 0%(0 out of 14657). But there is 11160 is '企业选择不公示'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    实际员工数量
    ------
    Empty percentage is 91%(13353 out of 14657). We just drop it.

    -----------------------------
    年报年份
    ------
    Empty percentage is 0%(0 out of 14657).
    There's no need to handle the empty.

    -----------------------------
    :return:
    """
    # EMPTY CHECK
    empty_check_list = [u'主营业务收入'.encode('utf-8'),
                        u'净利润'.encode('utf-8'),
                        u'利润总额'.encode('utf-8'),
                        u'所有者权益合计'.encode('utf-8'),
                        u'纳税总额'.encode('utf-8'),
                        u'营业总收入'.encode('utf-8'),
                        u'负债总额'.encode('utf-8'),
                        u'资产总额'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-企业资产状况信息.xlsx', columns=empty_check_list, thresh=3)

    # LIST OUT VALUES AFTER EMPTY ROWS HANDLED
    panaly.list_category_columns_values([u'年报-企业资产状况信息'], u'年报-企业资产状况信息_empty_handled',
                                        file_url=clean_data_temp_file_url)

    # COLUMNS HANDLE
    # 资产总额
    dcu.drop_unit(u'年报-企业资产状况信息', u'资产总额'.encode('utf-8'), [u'万元', u' 万元'])

    # 所有者权益合计
    dcu.drop_unit(u'年报-企业资产状况信息', u'所有者权益合计'.encode('utf-8'), [u'万元', u' 万元'])

    # 营业总收入
    dcu.drop_unit(u'年报-企业资产状况信息', u'营业总收入'.encode('utf-8'), [u'万元', u' 万元'])

    # 利润总额
    dcu.drop_unit(u'年报-企业资产状况信息', u'利润总额'.encode('utf-8'), [u'万元', u' 万元'])

    # 主营业务收入
    dcu.drop_unit(u'年报-企业资产状况信息', u'主营业务收入'.encode('utf-8'), [u'万元', u' 万元'])

    # 主营业务
    keywords = [u'农', u'土地', u'电器', u'光纤', u'电器', u'化学', u'医疗', u'药', u'信息', u'钢', u'乳', u'互联网', u'电机',
                u'自动化', u'交通', u'汽车', u'投资', u'园区', u'房地产', u'有线', u'日用', u'服饰', u'矿', u'开采', u'国有',
                u'酒', u'银行', u'金融', u'证券', u'航空', u'航天', u'采掘', u'发电', u'工程', u'制造']
    dcu.extract_keyword(u'年报-企业资产状况信息', u'主营业务'.encode('utf-8'), keywords)

    # 净利润
    dcu.drop_unit(u'年报-企业资产状况信息', u'净利润'.encode('utf-8'), [u'万元', u' 万元'])

    # 纳税总额
    dcu.drop_unit(u'年报-企业资产状况信息', u'纳税总额'.encode('utf-8'), [u'万元', u' 万元'])

    # 负债总额
    dcu.drop_unit(u'年报-企业资产状况信息', u'负债总额'.encode('utf-8'), [u'万元', u' 万元'])

    # 实际员工数量
    dcu.drop_columns(u'年报-企业资产状况信息', [u'实际员工数量'.encode('utf-8')])

    # 年报年份

    return


def empty_value_handle_out_invest_info():
    """
    Dirty value handle for table 年报-对外投资信息.xlsx.
    First we'll drop rows that empty value is too many.
    This table has too many empty values, but they should be indicating the number is 0 or not published
    instead of dirty value. We want the counted number of each company, so we don't drop rows here.
    We don't drop data in this table, just replace them with 0.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    投资金额
    ------
    Empty values replaced with 0.

    -----------------------------
    投资占比
    ------
    Empty values replaced with 0.
    There's some value are far greater than 100, and we think it's unreasonable, so we need to mark them -1.

    -----------------------------
    年报年份
    ------
    Empty replaced with 0, indicating it's a 'Unknown' value.

    -----------------------------
    :return:
    """

    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'年报-对外投资信息')
    df = df.fillna(0)
    file_utils.write_file(df, clean_data_temp_file_url, u'年报-对外投资信息')

    panaly.list_category_columns_values([u'年报-对外投资信息'], u'年报-对外投资信息_empty_handled',
                                        file_url=clean_data_temp_file_url)

    dcu.mark_invalid_num_data(u'年报-对外投资信息', u'投资占比'.encode('utf-8'), '>', 100)
    return


def empty_value_handle_out_warrant_info():
    """
    Dirty value handle for table 年报-的对外提供保证担保信息.xlsx.
    First we'll drop rows that empty value is too many.
    ['主债权数额','主债权种类','保证的方式']
    Once there are more than 3 empties in these 3 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    主债权数额
    ------
    Empty percentage is 0%(0 out of 6893).
    Other values are formatted with end '万元' or pure numbers, but there's some have blank between number and unit,
    we just drop the unit and clear the blanks.

    -----------------------------
    保证担保的范围
    ------
    Empty percentage is 91.47%(6305 out of 6893). We need to drop it.

    -----------------------------
    保证的期间
    ------
    Empty percentage is 0.0435%(3 out of 6893). We just make them the same with '企业选择不公示'.
    Other values mainly '期限'(6348 out of 6893), and we merge '期间','期限','限期' into one('期限'), also there's a few
    listed as time periods, we merge them into '期限' too. The other value is '未约定'.

    -----------------------------
    保证的方式
    ------
    Empty percentage is 0%(0 out of 6893).
    There are 6 values: ['0', '6', '一般保证', '企业选择不公示', '未约定', '连带保证'], cause '0','6','未约定' counts too
    small(59,1,38 separately), we merge them into 'Others'.

    -----------------------------
    主债权种类
    ------
    Empty percentage is 0%(0 out of 6893).
    There are 3 values: ['企业选择不公示', '其他', '合同'].

    -----------------------------
    履行债务的期限
    ------
    Empty percentage is 0.0145%(1 out of 6893).
    Mainly time periods, but the format is not uniformed, some are like '2018年03月24日-2020年11月24日',
    some '2018年03月24日-', some '2017年8月7日-2018年8月6日', some '2015-01-07至2016-01-07', some '2014-04-04~2016-04-04',
    some '-2018年09月29日' and 6 '-'s, also some are '期限' or '企业选择不公示'. We first format all the time periods into
    '2014/4/4~2016/4/4' so we can handle it properly later.

    -----------------------------
    年报年份
    ------
    Empty percentage is 0%(0 out of 6893).
    They are properly formatted.

    -----------------------------
    :return:
    """
    empty_check_list = [u'主债权数额'.encode('utf-8'),
                        u'主债权种类'.encode('utf-8'),
                        u'保证的方式'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-的对外提供保证担保信息.xlsx', columns=empty_check_list, thresh=3)
    panaly.list_category_columns_values([u'年报-的对外提供保证担保信息'], u'年报-的对外提供保证担保信息_empty_handled',
                                        file_url=clean_data_temp_file_url)

    # 保证担保的范围
    dcu.drop_columns(u'年报-的对外提供保证担保信息', [u'保证担保的范围'.encode('utf-8')])

    # 主债权数额
    dcu.drop_unit(u'年报-的对外提供保证担保信息', u'主债权数额'.encode('utf-8'), [u'万元', u' 万元'])

    # 保证的期间
    status_period = [u'期间', u'期限', u'限期']
    status_list = [status_period]
    status_after = [u'期间']
    dcu.merge_status(u'年报-的对外提供保证担保信息', u'保证的期间'.encode('utf-8'), status_list, status_after)

    # 保证的方式
    status_period = ['0', '6', u'未约定']
    status_list = [status_period]
    status_after = [u'Others']
    dcu.merge_status(u'年报-的对外提供保证担保信息', u'保证的方式'.encode('utf-8'), status_list, status_after)

    # 履行债务的期限
    dcu.time_periods_format(u'年报-的对外提供保证担保信息', u'履行债务的期限'.encode('utf-8'))

    return


def empty_value_handle_social_security_info():
    """
    Dirty value handle for table 年报-社保信息.xlsx.
    First we'll drop rows that empty value is too many.
    ['单位参加城镇职工基本养老保险累计欠缴金额','单位参加城镇职工基本养老保险缴费基数','单位参加失业保险累计欠缴金额',
    '单位参加失业保险缴费基数', '单位参加工伤保险累计欠缴金额','单位参加工伤保险缴费基数','单位参加生育保险缴费基数',
    '参加城镇职工基本养老保险本期实际缴费金额','工伤保险人数']
    Once there are more than 3 empties in these 9 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    城镇职工基本养老保险人数
    ------
    Empty percentage is 0.1265%(7 out of 5532). We mark them as -1.
    Other values are well formatted with end '人', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    失业保险人数
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1.
    Other values are well formatted with end '人', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    职工基本医疗保险人数
    ------
    Empty percentage is 0.1085%(6 out of 5532). We mark them as -1.
    Other values are well formatted with end '人', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    工伤保险人数
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1.
    Other values are well formatted with end '人', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    生育保险人数
    ------
    Empty percentage is 0.1085%(6 out of 5532). We mark them as -1.
    Other values are well formatted with end '人', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks.

    -----------------------------
    单位参加城镇职工基本养老保险缴费基数
    ------
    Empty percentage is 4.3745%(242 out of 5532). We mark them as -1. There is 592 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1.

    -----------------------------
    单位参加失业保险缴费基数
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1. There is 592 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1.

    -----------------------------
    单位参加职工基本医疗保险缴费基数
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1. There is 592 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1.

    -----------------------------
    单位参加工伤保险缴费基数
    ------
    Empty percentage is 96.9631%(5364 out of 5532). We need to drop this column.

    -----------------------------
    单位参加生育保险缴费基数
    ------
    Empty percentage is 0.0723%(4 out of 5532). We mark them as -1. There is 593 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1.

    -----------------------------
    参加城镇职工基本养老保险本期实际缴费金额
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1. There is 590 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(239) and we think them as missing, so they
    belong to -1.


    -----------------------------
    参加失业保险本期实际缴费金额
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1. There is 590 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(239) and we think them as missing, so they
    belong to -1.

    -----------------------------
    参加职工基本医疗保险本期实际缴费金额
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1. There is 590 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1.

    -----------------------------
    参加工伤保险本期实际缴费金额
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1. There is 590 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(313) and we think them as missing, so they
    belong to -1.

    -----------------------------
    参加生育保险本期实际缴费金额
    ------
    Empty percentage is 0.0904%(5 out of 5532). We mark them as -1. There is 590 is '企业选择不公示', and 325 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1.

    -----------------------------
    单位参加城镇职工基本养老保险累计欠缴金额
    ------
    Empty percentage is 0%(0 out of 5532). There is 596 is '企业选择不公示', and 324 '选择不公示',
    we merge them into 'NP'. Also there is one valued with minus number, we just remove the minus.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(240) and we think them as missing, so they
    belong to -1.

    -----------------------------
    单位参加失业保险累计欠缴金额
    ------
    Empty percentage is 0%(0 out of 5532). There is 596 is '企业选择不公示', and 324 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1. Also there is one valued with minus number, we just remove the minus.

    -----------------------------
    单位参加职工基本医疗保险累计欠缴金额
    ------
    Empty percentage is 0%(0 out of 5532). There is 596 is '企业选择不公示', and 324 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1. Also there is one valued with minus number, we just remove the minus.

    -----------------------------
    单位参加工伤保险累计欠缴金额
    ------
    Empty percentage is 0%(0 out of 5532). There is 600 is '企业选择不公示', and 324 '选择不公示',
    we merge them into 'NP'. Also there is one valued with minus number, we just remove the minus.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1. Also there is one valued with minus number, we just remove the minus.

    -----------------------------
    单位参加生育保险累计欠缴金额
    ------
    Empty percentage is 0%(0 out of 5532). There is 596 is '企业选择不公示', and 324 '选择不公示',
    we merge them into 'NP'.
    Other values are well formatted with end '万元', but there's some have blank between number and unit, we just
    drop the unit and clear the blanks. Be care we have some valued '万元'(235) and we think them as missing, so they
    belong to -1. Also there is one valued with minus number, we just remove the minus.

    -----------------------------
    年报年份
    ------
    Empty percentage is 0%(0 out of 5532).
    This is well formatted.

    -----------------------------
    :return:
    """
    empty_check_list = [u'单位参加城镇职工基本养老保险累计欠缴金额'.encode('utf-8'),
                        u'单位参加城镇职工基本养老保险缴费基数'.encode('utf-8'),
                        u'单位参加失业保险累计欠缴金额'.encode('utf-8'),
                        u'单位参加失业保险缴费基数'.encode('utf-8'),
                        u'单位参加工伤保险累计欠缴金额'.encode('utf-8'),
                        u'单位参加工伤保险缴费基数'.encode('utf-8'),
                        u'单位参加生育保险缴费基数'.encode('utf-8'),
                        u'城镇职工基本养老保险人数'.encode('utf-8'),
                        u'失业保险人数'.encode('utf-8'),
                        u'参加失业保险本期实际缴费金额'.encode('utf-8'),
                        u'参加工伤保险本期实际缴费金额'.encode('utf-8'),
                        u'参加城镇职工基本养老保险本期实际缴费金额'.encode('utf-8'),
                        u'工伤保险人数'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-社保信息.xlsx', columns=empty_check_list, thresh=3)
    panaly.list_category_columns_values([u'年报-社保信息'], u'年报-社保信息_empty_handled',
                                        file_url=clean_data_temp_file_url)

    dcu.drop_columns(u'年报-社保信息', [u'单位参加工伤保险缴费基数'.encode('utf-8')])

    status_np = [u'企业选择不公示', u'选择不公示']
    status_list = [status_np]
    status_after = ['NP']

    file_people_list = [u'城镇职工基本养老保险人数'.encode('utf-8'),
                        u'失业保险人数'.encode('utf-8'),
                        u'职工基本医疗保险人数'.encode('utf-8'),
                        u'工伤保险人数'.encode('utf-8'),
                        u'生育保险人数'.encode('utf-8')]
    file_cash_list = [u'单位参加城镇职工基本养老保险缴费基数'.encode('utf-8'),
                      u'单位参加失业保险缴费基数'.encode('utf-8'),
                      u'单位参加职工基本医疗保险缴费基数'.encode('utf-8'),
                      u'单位参加生育保险缴费基数'.encode('utf-8'),
                      u'参加城镇职工基本养老保险本期实际缴费金额'.encode('utf-8'),
                      u'参加失业保险本期实际缴费金额'.encode('utf-8'),
                      u'参加职工基本医疗保险本期实际缴费金额'.encode('utf-8'),
                      u'参加工伤保险本期实际缴费金额'.encode('utf-8'),
                      u'参加生育保险本期实际缴费金额'.encode('utf-8'),
                      u'单位参加城镇职工基本养老保险累计欠缴金额'.encode('utf-8'),
                      u'单位参加失业保险累计欠缴金额'.encode('utf-8'),
                      u'单位参加职工基本医疗保险累计欠缴金额'.encode('utf-8'),
                      u'单位参加工伤保险累计欠缴金额'.encode('utf-8'),
                      u'单位参加生育保险累计欠缴金额'.encode('utf-8')]

    for column in file_people_list:
        dcu.merge_status(u'年报-社保信息', column, status_list, status_after)
        dcu.drop_unit(u'年报-社保信息', column, [u'人', u' 人'], empty_mask=-1)

    for column in file_cash_list:
        dcu.merge_status(u'年报-社保信息', column, status_list, status_after)
        dcu.drop_unit_remove_minus(u'年报-社保信息', column, [u'万元', u' 万元'], empty_mask=-1)

    return


def empty_value_handle_share_exchange_info():
    """
    Dirty value handle for table 年报-股东股权转让.xlsx.
    First we'll drop rows that empty value is too many.
    ['变更前股权比例','变更后股权比例','年报年份','股权变更日期']
    Once there are more than 2 empties in these 4 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    变更前股权比例
    ------
    Empty percentage is 0.3939%(17 out of 4316). We replace them as -1.
    The format is not uniformed. Some are formatted as '.07%', some are '0.07%' and some are '0.07'. We need to drop '%'
    and make all format as '0.07'. For numbers greater than 1, we mark them as -1.

    -----------------------------
    变更后股权比例
    ------
    Empty percentage is 0.278%(12 out of 4316). We replace them as -1.
    The format is not uniformed. Some are formatted as '.07%', some are '0.07%' and some are '0.07'. We need to drop '%'
    and make all format as '0.07'. For numbers greater than 1, we mark them as -1.
    A more complicate problem is some value are actually belong to '股权变更日期', which we need to copy them to column
    '股权变更日期'

    -----------------------------
    股权变更日期
    ------
    Empty percentage is 0.3939%(17 out of 4316). The empty value are replaced to the invalid value('1000-01-01')
    so we can handle it later.
    Others are well formatted with format yyyy-mm-dd.

    -----------------------------
    年报年份
    ------
    Empty percentage is 0.139%(6 out of 4316). The empty value are replaced to the invalid value('1000')
    so we can handle it later.
    Others are well formatted with format yyyy-mm-dd.

    -----------------------------
    :return:
    """
    empty_check_list = [u'变更前股权比例'.encode('utf-8'),
                        u'变更后股权比例'.encode('utf-8'),
                        u'年报年份'.encode('utf-8'),
                        u'股权变更日期'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-股东股权转让.xlsx', columns=empty_check_list, thresh=2)
    panaly.list_category_columns_values([u'年报-股东股权转让'], u'年报-股东股权转让_empty_handled',
                                        file_url=clean_data_temp_file_url)

    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'年报-股东股权转让')
    values = {u'变更前股权比例'.encode('utf-8'): -1, u'变更后股权比例'.encode('utf-8'): -1,
              u'股权变更日期'.encode('utf-8'): '1000-01-01', u'年报年份'.encode('utf-8'): '1000'}
    for index in range(0, len(df)):
        content = df.at[index, u'股权变更日期'.encode('utf-8')]
        content_b = df.at[index, u'变更后股权比例'.encode('utf-8')]
        if '-' in str(content_b) and (pandas.isnull(content) or pandas.isna(content)):
            df.set_value(index, u'股权变更日期'.encode('utf-8'), content_b)
            df.set_value(index, u'变更后股权比例'.encode('utf-8'), '')

    df = df.fillna(values)
    file_utils.write_file(df, clean_data_temp_file_url, u'年报-股东股权转让')

    dcu.drop_unit_with_float_format(u'年报-股东股权转让', u'变更前股权比例'.encode('utf-8'), ['%'], empty_mask=-1)
    dcu.drop_unit_with_float_format(u'年报-股东股权转让', u'变更后股权比例'.encode('utf-8'), ['%'], empty_mask=-1)

    dcu.mark_invalid_num_data(u'年报-股东股权转让', u'变更前股权比例'.encode('utf-8'), '>', 100)
    dcu.mark_invalid_num_data(u'年报-股东股权转让', u'变更后股权比例'.encode('utf-8'), '>', 100)

    return


def empty_value_handle_share_holder_info():
    """
        Dirty value handle for table 年报-股东（发起人）及出资信息_rearranged.xlsx.
    First we'll drop rows that empty value is too many.
    ['实缴出资额（万元）','实缴出资方式','实缴出资日期','认缴出资方式', '认缴出资日期','认缴出资额（万元）']
    Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    股东类型
    ------
    Empty percentage is 95.8587%(76547 out of 79854). We need to drop it.

    -----------------------------
    股东所占比例
    ------
    Empty percentage is 98.7815263%(78881 out of 79854). We need to drop it.

    -----------------------------
    认缴出资方式
    ------
    Empty percentage is 2.3418%(1870 out of 79854). We replace them with -1.
    It's too complicate, we just count the item values here(may named as '认缴出资方式种类数'). So we just separate them
    with [',', '、'], to do this, we should drop the ',' or '、' at the end first.

    -----------------------------
    认缴出资额（万元）
    ------
    Empty percentage is 0.0288%(23 out of 79854). We just replace them with -1.
    We need to drop the unit ['万', '万元', '万元人民币', '万人民币'], and update ['万美元'] with the number multiplied
    by 6.7.

    -----------------------------
    认缴出资日期
    ------
    Empty percentage is 1.7344%(1385 out of 79854). We replace them by '1000-01-01'
    They are all formatted with format yyyy-mm-dd.
    But there are some are greater than 2019-03-01, we think they are invalid, so replace them as the same as empty.

    -----------------------------
    实缴出资方式
    ------
    Empty percentage is 5.9484%(4750 out of 79854). We replace them with -1.
    It's too complicate, we just count the item values here(may named as '认缴出资方式种类数'). So we just separate them
    with [',', '、', '，'], to do this, we should drop the ',' or '、' or '，' at the end first.

    -----------------------------
    实缴出资额（万元）
    ------
    Empty percentage is 3.2284%(2578 out of 79854). We just replace them with -1.
    We need to drop the unit ['万', '万元', '万元人民币', '万人民币'], and update ['万美元'] with the number multiplied
    by 6.7.

    -----------------------------
    实缴出资日期
    ------
    Empty percentage is 5.2558%(4197 out of 79854). We replace them by '1000-01-01'
    They are all formatted with format yyyy-mm-dd.
    But there are some are greater than 2019-03-01, we think they are invalid, so replace them as the same as empty.

    -----------------------------
    年报年份
    ------
    Empty percentage is 0.05009%(40 out of 79854). We replace them by '1000'

    -----------------------------
    :return:
    """
    empty_check_list = [u'实缴出资方式'.encode('utf-8'),
                        u'实缴出资日期'.encode('utf-8'),
                        u'实缴出资额（万元）'.encode('utf-8'),
                        u'认缴出资方式'.encode('utf-8'),
                        u'认缴出资日期'.encode('utf-8'),
                        u'认缴出资额（万元）'.encode('utf-8')]
    dcu.drop_rows_too_many_empty(u'年报-股东（发起人）及出资信息_rearranged.xlsx', columns=empty_check_list, thresh=2)
    panaly.list_category_columns_values([u'年报-股东（发起人）及出资信息_rearranged'], u'年报-股东（发起人）及出资信息_rearranged_empty_handled',
                                        file_url=clean_data_temp_file_url)

    dcu.drop_columns(u'年报-股东（发起人）及出资信息_rearranged', [u'股东类型'.encode('utf-8'), u'股东所占比例'.encode('utf-8')])

    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'年报-股东（发起人）及出资信息_rearranged')
    values = {u'认缴出资方式'.encode('utf-8'): -1, u'实缴出资方式'.encode('utf-8'): -1,
              u'认缴出资日期'.encode('utf-8'): '1000-01-01', u'实缴出资日期'.encode('utf-8'): '1000-01-01',
              u'认缴出资额（万元）'.encode('utf-8'): -1, u'实缴出资额（万元）'.encode('utf-8'): -1,
              u'年报年份'.encode('utf-8'): '1000'}
    df = df.fillna(values)
    file_utils.write_file(df, clean_data_temp_file_url, u'年报-股东（发起人）及出资信息_rearranged')

    # 认缴出资方式
    # 实缴出资方式
    splits = [',', u'、', u'，']
    dcu.drop_unit(u'年报-股东（发起人）及出资信息_rearranged', u'认缴出资方式'.encode('utf-8'), splits, empty_mask=-1)
    dcu.drop_unit(u'年报-股东（发起人）及出资信息_rearranged', u'实缴出资方式'.encode('utf-8'), splits, empty_mask=-1)

    dcu.count_split(u'年报-股东（发起人）及出资信息_rearranged', u'认缴出资方式'.encode('utf-8'), splits, empty_mask=-1)
    dcu.count_split(u'年报-股东（发起人）及出资信息_rearranged', u'实缴出资方式'.encode('utf-8'), splits, empty_mask=-1)

    # 认缴出资额（万元）
    # 实缴出资额（万元）
    dcu.drop_unit_with_transfer(u'年报-股东（发起人）及出资信息_rearranged', u'认缴出资额（万元）'.encode('utf-8'),
                                [u'万', u'万元', u'万元人民币', u'万人民币'], {u'万美元': 6.7}, empty_mask=-1)
    dcu.drop_unit_with_transfer(u'年报-股东（发起人）及出资信息_rearranged', u'实缴出资额（万元）'.encode('utf-8'),
                                [u'万', u'万元', u'万元人民币', u'万人民币'], {u'万美元': 6.7}, empty_mask=-1)

    return


def numeric_handle_basic_info():
    """
    numeric data for table 年报-企业基本信息.
    :return:
    """
    print 'mmmmm'


def work_():
    empty_value_handle_social_security_info()
    print('empty_value_handle_social_security_info() done!')
    empty_value_handle_share_exchange_info()
    print('empty_value_handle_share_exchange_info() done!')
    empty_value_handle_share_holder_info()
    print('empty_value_handle_share_holder_info() done!')
    return


def primary_analysis_after_empty_handled():
    """
    primary analysis after empty data handled
    :return:
    """
    panaly.list_category_columns_values(category_annual_report_files, u'年报类_empty_handled',
                                        file_url=clean_data_temp_file_url)
    return
