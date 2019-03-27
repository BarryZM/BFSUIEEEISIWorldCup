# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis) for annual reports data.
 including:
    年报-企业基本信息
    年报-企业资产状况信息
    年报-对外投资信息
    年报-的对外提供保证担保信息
    年报-社保信息
    年报-网站或网点信息
    年报-股东股权转让
    年报-股东（发起人）及出资信息
"""
import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url
import pandas as pd
import exploratory_data_utils as edu


def generate_index_basic_info(corporate_start, corporate_end):
    """
    ***年报-企业基本信息***

    指标1：企业是否有投资信息或购买其他公司股权，按年份：[2014, 2015, 2016, 2017]，总计4个，类别型--（0：Yes，1：No，-1：Unknown）
            列名：is_inv_or_buy_share_201x.
    指标2：企业经营状态，按年份：[2014, 2015, 2016, 2017]，总计4个，类别型--（0：正常经营，1：非正常经营，-1：Unknown）
            列名：man_form_201x.
    指标3：是否提供对外担保，按年份：[2014, 2015, 2016, 2017]，总计4个，类别型--（0：Yes，1：No，-1：Unknown）
            列名：is_out_ensure_201x.
    指标4：是否有网站或网点，按年份：[2014, 2015, 2016, 2017]，总计4个，类别型--（0：Yes，1：No，-1：Unknown）
            列名：is_website_201x.
    指标5：有限责任公司本年度是否发生股东股权转，按年份：[2014, 2015, 2016, 2017]，总计4个，类别型--（0：Yes，1：No，-1：Unknown）
            列名：is_share_changed_201x.

    共计20个指标
    :return:
    """
    columns = ['is_inv_or_buy_share_2014',
               'is_inv_or_buy_share_2015',
               'is_inv_or_buy_share_2016',
               'is_inv_or_buy_share_2017',
               'man_form_2014',
               'man_form_2015',
               'man_form_2016',
               'man_form_2017',
               'is_out_ensure_2014',
               'is_out_ensure_2015',
               'is_out_ensure_2016',
               'is_out_ensure_2017',
               'is_website_2014',
               'is_website_2015',
               'is_website_2016',
               'is_website_2017',
               'is_share_changed_2014',
               'is_share_changed_2015',
               'is_share_changed_2016',
               'is_share_changed_2017'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-企业基本信息')

    # for corporate in range(corporate_start, corporate_end + 1):columns
    for corporate in range(corporate_start, corporate_end):
        row_dict = {}
        row_list = []

        for year in range(2014, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'年报年份'.encode('utf-8')] == year]

            inline_columns = [u'企业是否有投资信息或购买其他公司股权'.encode('utf-8'),
                              u'企业经营状态'.encode('utf-8'),
                              u'是否提供对外担保'.encode('utf-8'),
                              u'是否有网站或网点'.encode('utf-8'),
                              u'有限责任公司本年度是否发生股东股权转'.encode('utf-8')]
            inline_map = {'Yes': 0, 'No': 1, 'Unknown': -1, u'正常经营': 0, u'非正常经营': 1}
            row_list += edu.category_num_counts(df_temp, inline_columns, inline_map)

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-企业基本信息_index', index=True)
    return


def generate_index_basic_info_work():
    generate_index_basic_info(1001, 4001)
    return
