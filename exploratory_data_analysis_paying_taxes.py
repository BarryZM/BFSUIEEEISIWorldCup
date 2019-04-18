# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis)
"""
import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url,  working_file_url
from files_category_info import category_paying_taxes
import pandas as pd
import exploratory_data_utils as edu
import visualize_utils as vu
import data_clean_utils as dcu

def generate_index_good_tax_year(corporate_start, corporate_end):

    """
    ***纳税A级年份***
    指标1：公司2014-2017是否有纳税A级年份，总计4个，int
    :return:
    """


    columns = ['A_taxer_2014',
               'A_taxer_2015',
               'A_taxer_2016',
               'A_taxer_2017']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'纳税A级年份')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0

        # 企业纳税A级年份数计算
        for year in range(2014, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'纳税A级年份'.encode('utf-8')] == year]
            row_list.append(len(df_temp))
            total_num1 += len(df_temp)

        row_dict[corporate] = row_list

        # print(len(row_list))
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'纳税A级年份_index', index=True)
    return


def generate_index_general_taxer(corporate_start, corporate_end):

    """
    ***专利***
    指标1：企业具有纳税人资格的个数，总计1个，int
    指标2：企业拥有的不同种类纳税人资格数量，总计4个，int
    指标3：纳税人状态为注销或报验个数，总计1个，int
    指标4：纳税公司不同注册类型个数，总计6个，int
    指标5：出口退（免）税企业数，总计1个，int
    指标6：认定时间在2000年前，2000-2010,2010年后的个数，总计3个，int
    :return:
    """



    columns = ['taxer_count',
               'kind_taxer_1',
               'kind_taxer_2',
               'kind_taxer_3',
               'kind_taxer_4',
               'status_cancel_or_inspire',
               'register_1',
               'register_2',
               'register_3',
               'register_4',
               'register_5',
               'register_6',
               'export_tax_rebate',
               'identify_year_before_2000',
               'identify_year_between_2000_and_2010',
               'identify_year_after_2010',]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'一般纳税人')
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

        # 企业纳税人资格数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 企业拥有的不同种类纳税人资格数量
        for kind in range(1, 5):
            y_df = df_temp.loc[df_temp[u'纳税人资格'.encode('utf-8')] == kind, u'纳税人资格'.encode(
                'utf-8')]
            row_list.append(len(y_df))
            total_num2 += len(df_temp)


        # 纳税人状态为注销或报验个数
        y_df = df_temp.loc[df_temp[u'纳税人状态'.encode('utf-8')] >= 2, u'纳税人状态'.encode('utf-8')]
        row_list.append(len(y_df))
        total_num3 += len(df_temp)

        # 纳税公司不同注册类型个数
        for kind in range(1, 7):
            y_df = df_temp.loc[df_temp[u'登记注册类型'.encode('utf-8')] == kind, u'登记注册类型'.encode('utf-8')]
            row_list.append(len(y_df))
            total_num4 += len(df_temp)


        # 出口退（免）税企业数
        y_df = df_temp.loc[df_temp[u'出口状态备案状态'.encode('utf-8')] == 1, u'出口状态备案状态'.encode('utf-8')]
        row_list.append(len(y_df))
        total_num5 += len(df_temp)

        # 认定日期在2000年前
        y_df = df_temp.loc[(df_temp['year0'] > 1000) & (df_temp['year0'] <= 2000)]
        row_list.append(len(y_df))
        total_num6 += len(df_temp)

        # 认定日期在2000年-2010年之间
        y_df = df_temp.loc[(df_temp['year0'] > 2000) & (df_temp['year0'] <= 2010)]
        row_list.append(len(y_df))
        total_num7 += len(df_temp)

        # 认定日期在2010年之后
        y_df = df_temp.loc[df_temp['year0'] > 2010]
        row_list.append(len(y_df))
        total_num8 += len(df_temp)

        row_dict[corporate] = row_list

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'一般纳税人_index', index=True)
    return


def append_score():
    """
    append score to each index file.
    :return:
    """
    score_frame = fu.read_file_to_df(working_file_url, u'企业评分')
    score_frame = score_frame.set_index(u'企业编号'.encode('utf-8'))

    for file_n in category_paying_taxes:
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
    for file_n in category_paying_taxes:
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
    for file_n in category_paying_taxes:
        print file_n

        data_frame = fu.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame['int_score'] = data_frame[u'企业总评分'.encode('utf-8')].apply(lambda x: round(x))

        fu.write_file(data_frame, corporation_index_file_url, file_n + '_index')


def pic_scatter():
    """
    plot scatter pictures for each index and score.
    :return:
    """
    vu.pic_scatter(category_paying_taxes, 'paying_taxes')

#
# indexes_filter = ['financing_count',
#                   'invest_year_between_2009_and_2013',
#                   'investment_amount_between_100million_and_500_million',
#                   'investment_amount_less_than_100_million',
#                   'investment_amount_more_than_500_million',
#                   'investment_year_after_2013',000
#                   'investment_year_before_2009'
#                   ]


indexes_filter = []


def drop_useless_indexes_first_stage():
    edu.drop_useless_indexes(category_paying_taxes, indexes_filter)






