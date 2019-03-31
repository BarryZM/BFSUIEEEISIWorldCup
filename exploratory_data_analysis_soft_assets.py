# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis) for soft assets data.
 including:
    专利
    产品
    作品著作权
    商标
    资质认证
    软著著作权
    项目信息
"""
import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url, corporate_index_false, corporate_index_true
import pandas as pd
import exploratory_data_utils as edu
import data_clean_utils as dcu
from dateutil import parser


def generate_index_patent(corporate_start, corporate_end):
    """
    ***专利***
    指标1：专利总数，总计1个，int
    指标2：分年专利数，[pre_2001, pre_2010, 2010-2013, 2014, 2015, 2016, 2017, 2018, 2019]总计9个，int
    指标3：分专利类型专利数，总计3个，int
    指标4：专利2018年增长率（2018/2017-1），总计1个，int
    指标4：专利2017年增长率（2017/2016-1），总计1个，int
    指标4：专利2016年增长率（2016/2015-1），总计1个，int
    :return:
    """
    # numeric first
    # status_1 = [u'发明专利', u'发明公布', u'发明公布更正', u'发明授权', u'发明授权更正']
    # status_2 = [u'外观设计', u'外观设计更正']
    # status_3 = [u'实用新型', u'实用新型更正']
    # status_list = [status_1, status_2, status_3]
    # status_after = [0, 1, 2]
    # dcu.merge_status(u'专利', u'专利类型'.encode('utf-8'), status_list, status_after)

    columns = ['patent_count_total',
               'patent_count_pre_2001',
               'patent_count_pre_2010',
               'patent_count_2010-13',
               'patent_count_2014',
               'patent_count_2015',
               'patent_count_2016',
               'patent_count_2017',
               'patent_count_2018',
               'patent_count_2019',
               'fm_patent_count',
               'wg_patent_count',
               'sy_patent_count'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'专利')

    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        df_temp = data_frame[data_frame[corporate_index_false] == corporate]
        df_temp['year'] = df_temp[u'申请日'.encode('utf-8')].apply(lambda x: parser.parse(x).year)

        row_list.append(len(df_temp))

        for year in [2001, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2019]:
            if year == 2001:
                df_y_temp = df_temp[df_temp['year'] < 2001]
            elif year == 2010:
                df_y_temp = df_temp[df_temp['year'] < 2010]
            elif year == 2013:
                df_y_temp = df_temp[df_temp['year'] < 2013][df_temp['year'] > 2010]
            else:
                df_y_temp = df_temp[df_temp['year'] == year]
            row_list.append(len(df_y_temp))

        for category in [0, 1, 2]:
            df_ca_temp = df_temp[df_temp[u'专利类型'.encode('utf-8')] == category]
            row_list.append(len(df_ca_temp))

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)
    #
    # dis_df['growth_rate_2018'] = dis_df.apply(lambda x: x['patent_count_2018'] / x['patent_count_2017'] - 1, axis=1)
    # dis_df['growth_rate_2017'] = dis_df.apply(lambda x: x['patent_count_2017'] / x['patent_count_2016'] - 1, axis=1)
    # dis_df['growth_rate_2016'] = dis_df.apply(lambda x: x['patent_count_2016'] / x['patent_count_2015'] - 1, axis=1)

    fu.write_file(dis_df, corporation_index_file_url, u'专利_index', index=True)
    return


def generate_index_patent_work():
    generate_index_patent(1001, 4000)
    return


def generate_index_products(corporate_start, corporate_end):
    """
    ***产品***
    指标1：拥有产品数，总计1个，int
    指标2：拥有产品类别数，总计1个，int
    指标3：分产品类型产品数，总计6个，int

    总计8个
    :return:
    """
    columns = ['products_total',
               'products_categories_count',
               'android_count',
               'ios_count',
               'miniapp_count',
               'website_count',
               'wechat_count',
               'weibo_count'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'产品')

    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        df_temp = data_frame[data_frame[corporate_index_true] == corporate]

        row_list.append(len(df_temp))
        value = df_temp.nunique().get(u'产品类型'.encode('utf-8'))
        if not isinstance(value, int):
            value = 0
        row_list.append(value)

        for category in ['android', 'ios', 'miniapp', 'website', 'wechat', 'weibo']:
            df_c_temp = df_temp[df_temp[u'产品类型'.encode('utf-8')] == category]
            row_list.append(len(df_c_temp))

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'产品_index', index=True)
    return


def generate_index_products_work():
    generate_index_products(1001, 4000)
    return
