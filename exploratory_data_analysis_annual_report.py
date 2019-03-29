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
    for corporate in range(corporate_start, corporate_end + 1):
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
            row_list += edu.category_mapping(df_temp, inline_columns, inline_map)

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-企业基本信息_index', index=True)
    return


def generate_index_basic_info_work():
    generate_index_basic_info(1001, 4000)
    return


def generate_index_assets_info(corporate_start, corporate_end):
    """
    ***年报-企业资产状况信息***

    指标1：主营业务收入是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）
    指标2：净利润是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）
    指标3：利润总额是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）
    指标4：所有者权益合计是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）
    指标5：纳税总额是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）
    指标6：营业总收入是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）
    指标7：负债总额是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）
    指标8：资产总额是否公布，按年份：[2014, 2015, 2016, 2017]，总计4个，bool--（0：公布，1：不公布）

    共计32个指标
    :param corporate_start:
    :param corporate_end:
    :return:
    """
    columns = ['is_pub_main_in_2014',
               'is_pub_main_in_2015',
               'is_pub_main_in_2016',
               'is_pub_main_in_2017',
               'is_pub_net_in_2014',
               'is_pub_net_in_2015',
               'is_pub_net_in_2016',
               'is_pub_net_in_2017',
               'is_pub_total_in_2014',
               'is_pub_total_in_2015',
               'is_pub_total_in_2016',
               'is_pub_total_in_2017',
               'is_pub_holder_in_2014',
               'is_pub_holder_in_2015',
               'is_pub_holder_in_2016',
               'is_pub_holder_in_2017',
               'is_pub_tax_2014',
               'is_pub_tax_2015',
               'is_pub_tax_2016',
               'is_pub_tax_2017',
               'is_pub_total_in_2014',
               'is_pub_total_in_2015',
               'is_pub_total_in_2016',
               'is_pub_total_in_2017',
               'is_pub_debt_2014',
               'is_pub_debt_2015',
               'is_pub_debt_2016',
               'is_pub_debt_2017',
               'is_pub_asset_2014',
               'is_pub_asset_2015',
               'is_pub_asset_2016',
               'is_pub_asset_2017'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-企业资产状况信息')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        for year in range(2014, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'年报年份'.encode('utf-8')] == year]

            inline_columns = [u'主营业务收入'.encode('utf-8'),
                              u'净利润'.encode('utf-8'),
                              u'利润总额'.encode('utf-8'),
                              u'所有者权益合计'.encode('utf-8'),
                              u'纳税总额'.encode('utf-8'),
                              u'营业总收入'.encode('utf-8'),
                              u'负债总额'.encode('utf-8'),
                              u'资产总额'.encode('utf-8')]
            inline_map = {u'企业选择不公示': 1}
            row_list += edu.category_mapping(df_temp, inline_columns, inline_map, unknown=1, others=0)

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-企业资产状况信息_index', index=True)
    return


def generate_index_assets_info_work():
    generate_index_assets_info(1001, 4000)
    return


def generate_index_out_invest_info(corporate_start, corporate_end):
    """
    ***年报-对外投资信息***

    指标1：投资笔数，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，int
    指标1.1：总投资笔数，共1个，int
    指标2：最大投资占比，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标2.1：超过50%投资占比，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标3：投资金额总数，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标4：最大笔投资金额，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float

    共计26个指标
    :param corporate_start:
    :param corporate_end:
    :return:
    """
    columns = ['is_pub_main_in_2014',
               'is_pub_main_in_2015',
               'is_pub_main_in_2016',
               'is_pub_main_in_2017',
               'is_pub_net_in_2014',
               'is_pub_net_in_2015',
               'is_pub_net_in_2016',
               'is_pub_net_in_2017',
               'is_pub_total_in_2014',
               'is_pub_total_in_2015',
               'is_pub_total_in_2016',
               'is_pub_total_in_2017',
               'is_pub_holder_in_2014',
               'is_pub_holder_in_2015',
               'is_pub_holder_in_2016',
               'is_pub_holder_in_2017',
               'is_pub_tax_2014',
               'is_pub_tax_2015',
               'is_pub_tax_2016',
               'is_pub_tax_2017',
               'is_pub_total_in_2014',
               'is_pub_total_in_2015',
               'is_pub_total_in_2016',
               'is_pub_total_in_2017',
               'is_pub_debt_2014',
               'is_pub_debt_2015',
               'is_pub_debt_2016',
               'is_pub_debt_2017',
               'is_pub_asset_2014',
               'is_pub_asset_2015',
               'is_pub_asset_2016',
               'is_pub_asset_2017'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-企业资产状况信息')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        for year in range(2014, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'年报年份'.encode('utf-8')] == year]

            inline_columns = [u'主营业务收入'.encode('utf-8'),
                              u'净利润'.encode('utf-8'),
                              u'利润总额'.encode('utf-8'),
                              u'所有者权益合计'.encode('utf-8'),
                              u'纳税总额'.encode('utf-8'),
                              u'营业总收入'.encode('utf-8'),
                              u'负债总额'.encode('utf-8'),
                              u'资产总额'.encode('utf-8')]
            inline_map = {u'企业选择不公示': 1}
            row_list += edu.category_mapping(df_temp, inline_columns, inline_map, unknown=1, others=0)

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-企业资产状况信息_index', index=True)
    return


def generate_index_out_invest_info_work():
    generate_index_assets_info(1001, 4000)
    return
