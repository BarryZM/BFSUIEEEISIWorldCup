# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis)
"""

import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url, working_file_url
import pandas as pd
from files_category_info import category_basic_information
import data_clean_utils as dcu
import visualize_utils as vu
import exploratory_data_utils as edu


def generate_index_basic_info():

    """
    ***工商基本信息表***
    指标1：注册资本（万元），总计3000个，int
    指标2：经营状态，总计4个，int
    指标3：行业大类（代码），总计18个，int
    指标4：行业小类（代码），总计80个，int
    指标5：类型，总计2个，int
    指标6：省份代码，总计32个，int
    指标7：是否上市，总计2个，int
    指标8：员工人数，总计41个，int
    指标9：公司存在时间
    指标10：公司是否注销，总计2个，int

    :return:
    """

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'工商基本信息表')


    data_frame.rename(columns={u'企业编号'.encode('utf-8'): 'Unnamed: 0',
                               u'注册资本币种(正则)'.encode('utf-8'): 'type_of_currency',
                               u'注册资本（万元）'.encode('utf-8'): 'register_capital',
                               u'经营状态'.encode('utf-8'): 'running_status',
                               u'行业大类（代码）'.encode('utf-8'): 'industry category',
                               u'行业小类（代码）'.encode('utf-8'): 'industry subgroup',
                               u'类型'.encode('utf-8'): 'type',
                               u'省份代码'.encode('utf-8'): 'province_code',
                               u'是否上市'.encode('utf-8'): 'list_shares_or_not',
                               u'员工人数'.encode('utf-8'): 'staff_number'}, inplace=True)


    # 公司资本的人民币化处理
    # 将column2 中某些行（通过column1中的value1来过滤出来的）的值为value2
    data_frame.loc[data_frame['type_of_currency'] == 2, 'register_capital'] = data_frame.register_capital.apply(lambda x: x * 6.7)
    data_frame.drop('type_of_currency', axis=1, inplace=True)

    # 公司存在时间
    data_frame["year_2019"] = 2019 # 生成新列2019
    # 用将2019年份列与公司成立年份列相减，形成存在时间,其中x带表当前行，可以通过下标进行索引
    data_frame['exist_year'] = data_frame.apply(lambda x: x['year_2019'] - x['year0'], axis=1)

    # 公司是否注销
    # 将column2 中某些行（通过column1中的value1来过滤出来的）的值为value2
    # 正常公司为1，注销公司为0
    data_frame['log_out_or_not'] = 0
    data_frame.loc[((data_frame[u'注销原因'.encode('utf-8')] == -1) & (data_frame[u'注销时间'.encode('utf-8')]== -1)), 'log_out_or_not'] = 1
    data_frame.drop([u'注销原因'.encode('utf-8'), u'注销时间'.encode('utf-8')], axis=1, inplace=True)

    data_frame.drop(['month0', 'day0'], axis=1, inplace=True)

    fu.write_file(data_frame, corporation_index_file_url, u'工商基本信息表_index', index=True)
    return

def generate_index_custom_credit(corporate_start, corporate_end):

    """
    ***海关进出口信用***
    指标1：经济区划，总计8个，int
    指标2：经营类别，总计6个，int
    指标3：有海关注销标志企业，总计1个，int
    指标4：年报情况，总计5个，int
    指标5：信用等级，总计4个，int
    :return:
    """



    columns = ['kind_of_range_1',
               'kind_of_range_2',
               'kind_of_range_3',
               'kind_of_range_4',
               'kind_of_range_5',
               'kind_of_range_6',
               'kind_of_range_7',
               'kind_of_range_8',
               'kind_of_tax_company_1',
               'kind_of_tax_company_2',
               'kind_of_tax_company_3',
               'kind_of_tax_company_4',
               'kind_of_tax_company_5',
               'kind_of_tax_company_6',
               'log_out_custom',
               'status_of_annual_report_1',
               'status_of_annual_report_2',
               'status_of_annual_report_3',
               'status_of_annual_report_4',
               'status_of_annual_report_5',
               'level_of_credit_1',
               'level_of_credit_2',
               'level_of_credit_3',
               'level_of_credit_4']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'海关进出口信用')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]


        # 经济区划
        for i in range(1,9):
            y_df = df_temp[df_temp[u'经济区划'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num1 += len(df_temp)

        # 经营类别
        for i in range(1, 7):
            y_df = df_temp[df_temp[u'经营类别'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num2 += len(df_temp)

        # print(len(row_list))


        # 有海关注销标志企业
        y_df = df_temp.loc[df_temp[u'海关注销标志'.encode('utf-8')] == 2, u'海关注销标志'.encode('utf-8')]
        row_list.append(len(y_df))
        total_num3 += len(df_temp)

        # print(len(row_list))

        # 年报情况
        for i in range(1, 5):
            y_df = df_temp[df_temp[u'年报情况'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num4 += len(df_temp)

        # 信用等级
        for i in range(1, 6):
            y_df = df_temp[df_temp[u'信用等级'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num5 += len(df_temp)

        row_dict[corporate] = row_list

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'海关进出口信用_index', index=True)
    return



def generate_index_tender(corporate_start, corporate_end):

    """
    ***招投标***
    指标1：公告类型，总计19个，int
    指标2：省份，总计34个，int
    指标3：中标或招标，总计2个，int
    指标4：年报情况，总计5个，int
    指标5：信用等级，总计4个，int
    :return:
    """



    columns = ['status_of_announcement_1',
               'status_of_announcement_2',
               'status_of_announcement_3',
               'status_of_announcement_4',
               'status_of_announcement_5',
               'status_of_announcement_6',
               'status_of_announcement_7',
               'status_of_announcement_8',
               'status_of_announcement_9',
               'status_of_announcement_10',
               'status_of_announcement_11',
               'status_of_announcement_12',
               'status_of_announcement_13',
               'status_of_announcement_14',
               'status_of_announcement_15',
               'status_of_announcement_16',
               'status_of_announcement_17',
               'status_of_announcement_18',
               'status_of_announcement_19',
               'province_11',
               'province_12',
               'province_13',
               'province_14',
               'province_15',
               'province_21',
               'province_22',
               'province_23',
               'province_31',
               'province_32',
               'province_33',
               'province_34',
               'province_35',
               'province_36',
               'province_37',
               'province_41',
               'province_42',
               'province_43',
               'province_44',
               'province_45',
               'province_46',
               'province_50',
               'province_51',
               'province_52',
               'province_53',
               'province_54',
               'province_61',
               'province_62',
               'province_63',
               'province_64',
               'province_65',
               'province_71',
               'province_81',
               'province_82',
               'bidding',
               'tendering',
               'announcement_year_before_2009',
               'announcement_year_2009_2013',
               'announcement_year_2013_2019']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'招投标')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]


        # 公告类型
        for i in range(1,20):
            y_df = df_temp[df_temp[u'公告类型'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num1 += len(df_temp)

        # 省份
        for i in (11, 12, 13, 14, 15, 21, 22, 23, 31, 32, 33, 34, 35, 36, 37, 41, 42, 43, 44, 45, 46, 50, 51, 52, 53, 54,
                   61, 62, 63, 64, 65, 71, 81, 82):
            y_df = df_temp[df_temp[u'省份'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num2 += len(df_temp)

        # 中标或招标
        for i in range(1,3):
            y_df = df_temp[df_temp[u'中标或招标'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)

        y_df = df_temp[(df_temp['year0'] <= 2009) & (df_temp['year0'] >1000)]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)

        y_df = df_temp[(df_temp['year0'] >2009) & (df_temp['year0'] <= 2013)]
        row_list.append(len(y_df))
        total_num5 += len(df_temp)

        y_df = df_temp[(df_temp['year0'] > 2013) & (df_temp['year0'] <= 2019)]
        row_list.append(len(y_df))
        total_num6 += len(df_temp)

        row_dict[corporate] = row_list

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'招投标_index', index=True)
    return




def generate_index_bond(corporate_start, corporate_end):

    """
    ***债券信息***
    指标1：企业拥有的不同债券评级数，总计7个，int
    指标2：债券期限小于1年或大于一年的数量，总计2个，int
    指标3：企业拥有的不同债券品种的数量，总计7个，int
    指标4：计划发行额度小于10亿或者大于10亿的数量，总计2个，int
    指标5：利率小于5%或者大于5%的数量，总计2个，int
    指标6：债券发行日期在2013年前和在2013年后的数量，总计2个，int
    指标7：债券兑付日期在2020年前和在2020年后的数量，总计2个，int
    :return:
    """



    columns = ['ranking_of_bond_1',
               'ranking_of_bond_2',
               'ranking_of_bond_3',
               'ranking_of_bond_4',
               'ranking_of_bond_5',
               'ranking_of_bond_6',
               'ranking_of_bond_7',
               'bond_duration_less_than_1_year',
               'bond_duration_longer_than_1_year',
               'kind_of_bond_1',
               'kind_of_bond_2',
               'kind_of_bond_3',
               'kind_of_bond_4',
               'kind_of_bond_5',
               'kind_of_bond_6',
               'kind_of_bond_7',
               'total_planned_issuance_less_than_one_billion',
               'total_planned_issuance_more_than_one_billion',
               'interest_rate_less_than_5%',
               'interest_rate_more_than_5%',
               'interest_pay_1',
               'interest_pay_2',
               'interest_pay_3',
               'interest_pay_4',
               'interest_pay_5',
               'interest_pay_6',
               'issuance_date_of_bonds_before_2013',
               'issuance_date_of_bonds_after_2013',
               'bond_payment_date_before_2020',
               'bond_payment_date_after_2020']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'债券信息')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0
        total_num7 = 0
        total_num8 = 0
        total_num9 = 0
        total_num10 = 0
        total_num11 = 0
        total_num12 = 0
        total_num13 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]


        # 债券信用评级
        for i in range(1,8):
            y_df = df_temp[df_temp[u'债券信用评级'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num1 += len(df_temp)

        # 债券期限小于一年
        y_df = df_temp[df_temp[u'债券期限'.encode('utf-8')] <= 1]
        row_list.append(len(y_df))
        total_num2 += len(df_temp)

        # 债券期限大于一年
        y_df = df_temp[df_temp[u'债券期限'.encode('utf-8')] > 1]
        row_list.append(len(y_df))
        total_num3 += len(df_temp)

        # 债券品种
        for i in range(1, 8):
            y_df = df_temp[df_temp[u'债券品种'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num4 += len(df_temp)

        # 计划发行总额小于10亿
        y_df = df_temp[df_temp[u'计划发行总额（亿元）'.encode('utf-8')] <= 10]
        row_list.append(len(y_df))
        total_num5 += len(df_temp)

        # 计划发行总额大于10亿
        y_df = df_temp[df_temp[u'计划发行总额（亿元）'.encode('utf-8')] > 10]
        row_list.append(len(y_df))
        total_num6 += len(df_temp)

        # 票面利率小于5%
        y_df = df_temp[df_temp[u'票面利率（%）'.encode('utf-8')] <= 5]
        row_list.append(len(y_df))
        total_num7 += len(df_temp)

        # 票面利率大于5%
        y_df = df_temp[df_temp[u'票面利率（%）'.encode('utf-8')] > 5]
        row_list.append(len(y_df))
        total_num8 += len(df_temp)

        # 付息方式
        for i in range(1, 7):
            y_df = df_temp[df_temp[u'付息方式'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num9 += len(df_temp)

        # 债券发行日期在2014年之前
        y_df = df_temp[(df_temp['year0'] <= 2013) & (df_temp['year0'] > 1000)]
        row_list.append(len(y_df))
        total_num11 += len(df_temp)

        # 债券发行日期在2014年及以后
        y_df = df_temp[df_temp['year0'] > 2013]
        row_list.append(len(y_df))
        total_num10 += len(df_temp)

        # 债券兑付日期在2020年之前
        y_df = df_temp[df_temp['year1'] <= 2020 & (df_temp['year1'] > 1000)]
        row_list.append(len(y_df))
        total_num13 += len(df_temp)

        # 债券兑付日期在2020年以后
        y_df = df_temp[df_temp['year1'] > 2020]
        row_list.append(len(y_df))
        total_num12 += len(df_temp)




        row_dict[corporate] = row_list

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'债券信息_index', index=True)
    return




def generate_index_financing(corporate_start, corporate_end):

    """
    ***融资信息***
    指标1：公司融资次数
    指标2：公司不同类型融资次数，总计29个，int
    指标3：公司投资金额小于1亿、在1亿和5亿之间、大于5亿，总计3个，int
    指标4：年报情况，总计5个，int
    指标5：信用等级，总计4个，int
    :return:
    """



    columns = ['financing_count',
               'round_1',
               'round_2',
               'round_3',
               'round_4',
               'round_5',
               'round_6',
               'round_7',
               'round_8',
               'round_9',
               'round_10',
               'round_11',
               'round_12',
               'round_13',
               'round_14',
               'round_15',
               'round_16',
               'round_17',
               'round_18',
               'round_19',
               'round_20',
               'round_21',
               'round_22',
               'round_23',
               'round_24',
               'round_25',
               'round_26',
               'round_27',
               'round_28',
               'round_29',
               'investment_amount_less_than_100_million',
               'investment_amount_between_100million_and_500_million',
               'investment_amount_more_than_500_million',
               'investment_year_before_2009',
               'invest_year_between_2009_and_2013',
               'investment_year_after_2013']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'融资信息')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0
        total_num7 = 0
        total_num8 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]

        # 公司融资次数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 公司融资轮次数
        for i in range(1,30):
            y_df = df_temp[df_temp[u'轮次'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num2 += len(df_temp)

        # 投资金额小于1亿
        y_df = df_temp[(df_temp[u'投资金额'.encode('utf-8')] > 0) & (df_temp[u'投资金额'.encode('utf-8')] <= 1000000000)]
        row_list.append(len(y_df))
        total_num3 += len(df_temp)

        # 投资金额在1亿和5亿之间
        y_df = df_temp[(df_temp[u'投资金额'.encode('utf-8')] > 100000000) & (df_temp[u'投资金额'.encode('utf-8')] <= 500000000)]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)

        # 投资金额大于5亿
        y_df = df_temp[df_temp[u'投资金额'.encode('utf-8')] > 500000000]
        row_list.append(len(y_df))
        total_num5 += len(df_temp)

        # 公司融资日期在2009年之前
        y_df = df_temp[(df_temp['year0'] > 1000) & (df_temp['year0'] < 2009)]
        row_list.append(len(y_df))
        total_num6 += len(df_temp)

        # 公司融资日期在2009年和2013年之间
        y_df = df_temp[(df_temp['year0'] >= 2009) & (df_temp['year0'] < 2013)]
        row_list.append(len(y_df))
        total_num7 += len(df_temp)

        # 公司融资日期在2013年之后
        y_df = df_temp[df_temp['year0'] >= 2013]
        row_list.append(len(y_df))
        total_num8 += len(df_temp)

        row_dict[corporate] = row_list

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'融资信息_index', index=True)
    return


def append_score():
    """
    append score to each index file.
    :return:
    """
    score_frame = fu.read_file_to_df(working_file_url, u'企业评分')
    score_frame = score_frame.set_index(u'企业编号'.encode('utf-8'))

    for file_n in category_basic_information:
        print file_n

        data_frame = fu.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame = data_frame.set_index('Unnamed: 0')

        data_frame = data_frame.join(score_frame)

        fu.write_file(data_frame, corporation_index_file_url, file_n + '_index', index=True)
    return


def drop_score_empty():
    """
    some corporates lack of scores, we need to drop them.
    :return:
    """
    empty_check_list = [u'企业总评分'.encode('utf-8')]
    for file_n in category_basic_information:
        print file_n

        dcu.merge_rows(file_n + '_index', file_url=corporation_index_file_url,
                       dst_file_url=corporation_index_file_url)
        dcu.drop_rows_too_many_empty(file_n + '_index', file_url=corporation_index_file_url,
                                     dst_file_url=corporation_index_file_url, columns=empty_check_list, thresh=1)


def score_integerize():
    """
    scores are float, and we want try if integers will helps.
    :return:
    """
    for file_n in category_basic_information:
        print file_n

        data_frame = fu.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame['int_score'] = data_frame[u'企业总评分'.encode('utf-8')].apply(lambda x: round(x))

        fu.write_file(data_frame, corporation_index_file_url, file_n + '_index')


def pic_scatter():
    """
    plot scatter pictures for each index and score.
    :return:
    """
    vu.pic_scatter(category_basic_information, 'basic_info')

#
# indexes_filter = ['financing_count',
#                   'invest_year_between_2009_and_2013',
#                   'investment_amount_between_100million_and_500_million',
#                   'investment_amount_less_than_100_million',
#                   'investment_amount_more_than_500_million',
#                   'investment_year_after_2013',
#                   'investment_year_before_2009'
#                   ]


indexes_filter = ['bidding',
                  'register_capital',
                  'status_of_announcement_1',
                  'status_of_announcement_3',
                  'status_of_announcement_4',
                  'status_of_announcement_6',
                  'status_of_announcement_7',
                  'status_of_announcement_8',
                  'status_of_announcement_18',
                  'province_11',
                  'province_15',
                  'province_23',
                  'province_33']


def drop_useless_indexes_first_stage():
    edu.drop_useless_indexes(category_basic_information, indexes_filter)
