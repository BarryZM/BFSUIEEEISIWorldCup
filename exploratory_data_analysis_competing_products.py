# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis)
"""




import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url, working_file_url
from files_category_info import category_competing_products
from file_directions import test_start
from file_directions import test_end
import pandas as pd
import exploratory_data_utils as edu
import visualize_utils as vu
import data_clean_utils as dcu


def generate_index_competing_products(corporate_start, corporate_end):

    """
    ***专利***
    指标1：竞品总数，总计1个，int
    指标2：竞品良好运营数，总计1个，int
    指标3：竞品聚集城市，总计3个，int
    指标4：竞品分行业总数，总计34个，int
    指标5：竞品融资状态数（before IPO/ after IPO），总计2个，int
    指标6：竞品成立时间在2000年前，2000-2010,2010年后的个数，总计3个，int
    :return:
    """



    columns = ['products_count',
               'products_status',
               'products_address_1',
               'products_address_2',
               'products_address_3',
               'products_industry_1',
               'products_industry_2',
               'products_industry_3',
               'products_industry_4',
               'products_industry_5',
               'products_industry_6',
               'products_industry_7',
               'products_industry_8',
               'products_industry_9',
               'products_industry_10',
               'products_industry_11',
               'products_industry_12',
               'products_industry_13',
               'products_industry_14',
               'products_industry_15',
               'products_industry_16',
               'products_industry_17',
               'products_industry_18',
               'products_industry_19',
               'products_industry_20',
               'products_industry_21',
               'products_industry_22',
               'products_industry_23',
               'products_industry_24',
               'products_industry_25',
               'products_industry_26',
               'products_industry_27',
               'products_industry_28',
               'products_industry_29',
               'products_industry_30',
               'products_industry_31',
               'products_industry_32',
               'products_industry_33',
               'products_industry_34',
               'products_before_IPO',
               'products_after_IPO',
               'products_set_up_before_2000',
               'products_set_up_between_2000_and_2010',
               'products_set_up_after_2010']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'竞品')
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

        # 公司拥有的竞品数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # print(len(row_list))

        # 良好运营竞品数（运营+融资）
        y_df = df_temp.loc[df_temp[u'竞品运营状态'.encode('utf-8')] >= 3, u'竞品运营状态'.encode('utf-8')]
        row_list.append(len(y_df))
        total_num2 += len(df_temp)

        # print(len(row_list))

        # 竞品聚集数量
        for i in range(1,4):
            y_df = df_temp.loc[df_temp[u'竞品详细地址'.encode('utf-8')] == i, u'竞品详细地址'.encode(
                'utf-8')]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)

        # print(len(row_list))

        # 公司不同行业竞品数
        for category in range(1, 35):
            df_c_temp = df_temp[df_temp[u'竞品的标签'.encode('utf-8')] == category]
            row_list.append(len(df_c_temp))

        # print(len(row_list))


        # 公司竞品融资轮次在第15类（IPO）之后
        y_df = df_temp.loc[df_temp[u'竞品运营状态'.encode('utf-8')] >= 15, u'竞品运营状态'.encode('utf-8')]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)

        # print(len(row_list))

        # 公司竞品融资轮次在第15类（IPO）之前
        y_df = df_temp.loc[df_temp[u'竞品运营状态'.encode('utf-8')] < 15, u'竞品运营状态'.encode('utf-8')]
        row_list.append(len(y_df))
        total_num5 += len(df_temp)

        # 竞品成立时间在2000年前
        y_df = df_temp.loc[(df_temp['year0'] > 1000) & (df_temp['year0'] <= 2000)]
        row_list.append(len(y_df))
        total_num6 += len(df_temp)

        # 竞品成立时间在2000年-2010年之间
        y_df = df_temp.loc[(df_temp['year0'] > 2000) & (df_temp['year0'] <= 2010)]
        row_list.append(len(y_df))
        total_num7 += len(df_temp)

        # 竞品成立时间在2010年之后
        y_df = df_temp.loc[df_temp['year0'] > 2010]
        row_list.append(len(y_df))
        total_num8 += len(df_temp)

        row_dict[corporate] = row_list

        # print(len(row_list))
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'竞品_index', index=True)
    return


def append_score():
    """
    append score to each index file.
    :return:
    """
    score_frame = fu.read_file_to_df(working_file_url, u'企业评分')
    score_frame = score_frame.set_index(u'企业编号'.encode('utf-8'))

    for file_n in category_competing_products:
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
    for file_n in category_competing_products:
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
    for file_n in category_competing_products:
        print file_n

        data_frame = fu.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame['int_score'] = data_frame[u'企业总评分'.encode('utf-8')].apply(lambda x: round(x))

        fu.write_file(data_frame, corporation_index_file_url, file_n + '_index')


def pic_scatter():
    """
    plot scatter pictures for each index and score.
    :return:
    """
    vu.pic_scatter(category_competing_products, 'competing_products')

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
    edu.drop_useless_indexes(category_competing_products, indexes_filter)