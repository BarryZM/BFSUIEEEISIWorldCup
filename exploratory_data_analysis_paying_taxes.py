# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis)
"""
import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url
import pandas as pd
import exploratory_data_utils as edu

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
               'export_tax_rebate']
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


        row_dict[corporate] = row_list

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'一般纳税人_index', index=True)
    return









