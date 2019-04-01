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
from file_directions import clean_data_temp_file_url, corporation_index_file_url, working_file_url
import pandas as pd
import exploratory_data_utils as edu
import data_clean_utils as dcu
from dateutil import parser


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
               'man_form_2014',
               'is_out_ensure_2014',
               'is_website_2014',
               'is_share_changed_2014',
               'is_inv_or_buy_share_2015',
               'man_form_2015',
               'is_out_ensure_2015',
               'is_website_2015',
               'is_share_changed_2015',
               'is_inv_or_buy_share_2016',
               'man_form_2016',
               'is_out_ensure_2016',
               'is_website_2016',
               'is_share_changed_2016',
               'is_inv_or_buy_share_2017',
               'man_form_2017',
               'is_out_ensure_2017',
               'is_website_2017',
               'is_share_changed_2017'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-企业基本信息')

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
               'is_pub_net_in_2014',
               'is_pub_total_in_2014',
               'is_pub_holder_in_2014',
               'is_pub_tax_2014',
               'is_pub_total_in_2014',
               'is_pub_debt_2014',
               'is_pub_asset_2014',
               'is_pub_main_in_2015',
               'is_pub_net_in_2015',
               'is_pub_total_in_2015',
               'is_pub_holder_in_2015',
               'is_pub_tax_2015',
               'is_pub_total_in_2015',
               'is_pub_debt_2015',
               'is_pub_asset_2015',
               'is_pub_main_in_2016',
               'is_pub_net_in_2016',
               'is_pub_total_in_2016',
               'is_pub_holder_in_2016',
               'is_pub_tax_2016',
               'is_pub_total_in_2016',
               'is_pub_debt_2016',
               'is_pub_asset_2016',
               'is_pub_main_in_2017',
               'is_pub_net_in_2017',
               'is_pub_total_in_2017',
               'is_pub_holder_in_2017',
               'is_pub_tax_2017',
               'is_pub_total_in_2017',
               'is_pub_debt_2017',
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
    指标2.1：总最大投资占比，总计1个，float
    指标2.2：超过50%投资占比笔数，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，int
    指标2.3：总超过50%投资占比笔数，总计1个，int
    指标3：投资金额总数，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标3.1：总投资金额总数，总计1个，float
    指标4：最大笔投资金额，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标4.1：总最大笔投资金额，总计1个，float

    共计30个指标
    :param corporate_start:
    :param corporate_end:
    :return:
    """
    columns = ['inv_count_2013',
               'max_inv_ratio_2013',
               'inv_over_50_count_2013',
               'inv_amount_2013',
               'max_inv_amount_2013',
               'inv_count_2014',
               'max_inv_ratio_2014',
               'inv_over_50_count_2014',
               'inv_amount_2014',
               'max_inv_amount_2014',
               'inv_count_2015',
               'max_inv_ratio_2015',
               'inv_over_50_count_2015',
               'inv_amount_2015',
               'max_inv_amount_2015',
               'inv_count_2016',
               'max_inv_ratio_2016',
               'inv_over_50_count_2016',
               'inv_amount_2016',
               'max_inv_amount_2016',
               'inv_count_2017',
               'inv_count_total',
               'max_inv_ratio_2017',
               'max_inv_ratio_total',
               'inv_over_50_count_2017',
               'inv_over_50_count_total',
               'inv_amount_2017',
               'inv_amount_total',
               'max_inv_amount_2017',
               'max_inv_amount_total'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-对外投资信息')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        for year in range(2013, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'年报年份'.encode('utf-8')] == year]

            # 投资笔数
            row_list.append(len(df_temp))
            total_num1 += len(df_temp)

            if year == 2017:
                row_list.append(total_num1)
                total_num1 = 0

            # 投资占比
            y_df = df_temp.loc[df_temp[u'投资占比'.encode('utf-8')] >= 0, u'投资占比'.encode('utf-8')]

            # 最大投资占比
            y_max = y_df.max()
            if y_max > total_num2:
                total_num2 = y_max
            row_list.append(y_max)
            if year == 2017:
                row_list.append(total_num2)
                total_num2 = 0

            # 超过50%投资占比笔数
            y_df = df_temp.loc[df_temp[u'投资占比'.encode('utf-8')] > 50, u'投资占比'.encode('utf-8')]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)

            if year == 2017:
                row_list.append(total_num3)
                total_num3 = 0

            # 投资金额总数
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'投资金额'.encode('utf-8')]
            row_list.append(amount)
            total_num4 += amount

            if year == 2017:
                row_list.append(total_num4)
                total_num4 = 0

            # 最大笔投资金额
            df_temp.loc['Row_max'] = df_temp.apply(lambda x: x.max())
            max_amount = df_temp.at['Row_max', u'投资金额'.encode('utf-8')]
            row_list.append(max_amount)
            if max_amount > total_num5:
                total_num5 = max_amount

            if year == 2017:
                row_list.append(total_num5)
                total_num5 = 0

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-对外投资信息_index', index=True)
    return


def generate_index_out_invest_info_work():
    generate_index_out_invest_info(1001, 4000)
    df = fu.read_file_to_df(corporation_index_file_url, u'年报-对外投资信息_index')
    df = df.fillna(0)
    fu.write_file(df, corporation_index_file_url, u'年报-对外投资信息_index')
    return


def generate_index_out_warrant_info(corporate_start, corporate_end):
    """
    ***年报-的对外提供保证担保信息***

    指标0：主债权笔数，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标0.1：主债权笔数，总计1个，float
    指标1：主债权总数额，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标1.1：主债权总数额，总计1个，float
    指标2：连带保证主债权数额，按年份：[2013, 2014, 2015, 2016, 2017]，总计5个，float
    指标2.1：连带保证主债权数额，总计1个，float

    共计18个指标
    :param corporate_start:
    :param corporate_end:
    :return:
    """

    # numeric first
    status_period = [u'企业选择不公示']
    status_list = [status_period]
    status_after = [0]
    dcu.merge_status(u'年报-的对外提供保证担保信息', u'主债权数额'.encode('utf-8'), status_list, status_after)

    columns = ['pri_cred_right_count_2013',
               'pri_cred_right_2013',
               'gar_pri_cred_right_2013',
               'pri_cred_right_count_2014',
               'pri_cred_right_2014',
               'gar_pri_cred_right_2014',
               'pri_cred_right_count_2015',
               'pri_cred_right_2015',
               'gar_pri_cred_right_2015',
               'pri_cred_right_count_2016',
               'pri_cred_right_2016',
               'gar_pri_cred_right_2016',
               'pri_cred_right_count_2017',
               'pri_cred_right_count_total',
               'pri_cred_right_2017',
               'pri_cred_right_total',
               'gar_pri_cred_right_2017',
               'gar_pri_cred_right_total'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-的对外提供保证担保信息')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []
        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        for year in range(2013, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'年报年份'.encode('utf-8')] == year]

            # 主债权笔数
            row_list.append(len(df_temp))
            total_num1 += len(df_temp)

            if year == 2017:
                row_list.append(total_num1)
                total_num1 = 0

            # 主债权总数额
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'主债权数额'.encode('utf-8')]
            if not pd.isna(amount):
                amount = long(amount)
            else:
                amount = 0
            row_list.append(amount)
            total_num2 += amount

            if year == 2017:
                row_list.append(total_num2)
                total_num2 = 0

            # 连带保证主债权数额
            df_temp = df_temp[df_temp[u'保证的方式'.encode('utf-8')] == u'连带保证']
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'主债权数额'.encode('utf-8')]
            if not pd.isna(amount):
                amount = long(amount)
            else:
                amount = 0
            row_list.append(amount)
            total_num3 += amount

            if year == 2017:
                row_list.append(total_num3)
                total_num3 = 0

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-的对外提供保证担保信息_index', index=True)
    return


def generate_index_out_warrant_info_work():
    generate_index_out_warrant_info(1001, 4000)
    df = fu.read_file_to_df(corporation_index_file_url, u'年报-的对外提供保证担保信息_index')
    df = df.fillna(0)
    fu.write_file(df, corporation_index_file_url, u'年报-的对外提供保证担保信息_index')
    return


def generate_index_social_security_info(corporate_start, corporate_end):
    """
    ***年报-社保信息***

    指标1：城镇职工基本养老保险人数，按年份：[2016, 2017]，总计2个，int
    指标2：失业保险人数，按年份：[2016, 2017]，总计2个，int
    指标3：职工基本医疗保险人数，按年份：[2016, 2017]，总计2个，int
    指标4：工伤保险人数，按年份：[2016, 2017]，总计2个，int
    指标5：生育保险人数，按年份：[2016, 2017]，总计2个，int
    指标6：单位参加城镇职工基本养老保险缴费基数，按年份：[2016, 2017]，总计2个，float
    指标7：单位参加失业保险缴费基数，按年份：[2016, 2017]，总计2个，float
    指标8：单位参加职工基本医疗保险缴费基数，按年份：[2016, 2017]，总计2个，float
    ** 指标9：单位参加工伤保险缴费基数，按年份：[2016, 2017]，总计2个，float --- dropped
    指标10：单位参加生育保险缴费基数，按年份：[2016, 2017]，总计2个，float
    指标11：参加城镇职工基本养老保险本期实际缴费金额，按年份：[2016, 2017]，总计2个，float
    指标12：参加失业保险本期实际缴费金额，按年份：[2016, 2017]，总计2个，float
    指标13：参加职工基本医疗保险本期实际缴费金额，按年份：[2016, 2017]，总计2个，float
    指标14：参加工伤保险本期实际缴费金额，按年份：[2016, 2017]，总计2个，float
    指标15：参加生育保险本期实际缴费金额，按年份：[2016, 2017]，总计2个，float
    指标16：单位参加城镇职工基本养老保险累计欠缴金额，按年份：[2016, 2017]，总计2个，float
    指标17：单位参加失业保险累计欠缴金额，按年份：[2016, 2017]，总计2个，float
    指标18：单位参加职工基本医疗保险累计欠缴金额，按年份：[2016, 2017]，总计2个，float
    指标19：单位参加工伤保险累计欠缴金额，按年份：[2016, 2017]，总计2个，float
    指标20：单位参加生育保险累计欠缴金额，按年份：[2016, 2017]，总计2个，float

    共计38个
    :param corporate_start:
    :param corporate_end:
    :return:
    """

    # numeric first
    status_period = ['Unknown', 'NP']
    status_list = [status_period]
    status_after = [-1, -2]
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
    for column in (file_people_list + file_cash_list):
        dcu.merge_status(u'年报-社保信息', column, status_list, status_after)

    columns = ['peo_endow_insure_2016',
               'peo_unemp_insure_2016',
               'peo_medic_insure_2016',
               'peo_injur_insure_2016',
               'peo_mater_insure_2016',
               'pay_base_endow_insure_2016',
               'pay_base_unemp_insure_2016',
               'pay_base_medic_insure_2016',
               'pay_base_mater_insure_2016',
               'real_pay_endow_insure_2016',
               'real_pay_unemp_insure_2016',
               'real_pay_medic_insure_2016',
               'real_pay_injur_insure_2016',
               'real_pay_mater_insure_2016',
               'integ_pay_endow_insure_2016',
               'integ_pay_unemp_insure_2016',
               'integ_pay_medic_insure_2016',
               'integ_pay_injur_insure_2016',
               'integ_pay_mater_insure_2016',
               'peo_endow_insure_2017',
               'peo_unemp_insure_2017',
               'peo_medic_insure_2017',
               'peo_injur_insure_2017',
               'peo_mater_insure_2017',
               'pay_base_endow_insure_2017',
               'pay_base_unemp_insure_2017',
               'pay_base_medic_insure_2017',
               'pay_base_mater_insure_2017',
               'real_pay_endow_insure_2017',
               'real_pay_unemp_insure_2017',
               'real_pay_medic_insure_2017',
               'real_pay_injur_insure_2017',
               'real_pay_mater_insure_2017',
               'integ_unpay_endow_insure_2017',
               'integ_unpay_unemp_insure_2017',
               'integ_unpay_medic_insure_2017',
               'integ_unpay_injur_insure_2017',
               'integ_unpay_mater_insure_2017'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-社保信息')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        for year in range(2016, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'年报年份'.encode('utf-8')] == year]
            df_temp = df_temp.reset_index()

            # 人数
            for column in file_people_list:
                if len(df_temp) > 0:
                    row_list.append(df_temp.at[0, column])
                else:
                    row_list.append(0)

            # 金额
            for column in file_cash_list:
                if len(df_temp) > 0:
                    row_list.append(df_temp.at[0, column])
                else:
                    row_list.append(0)

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-社保信息_index', index=True)
    return


def generate_index_social_security_info_work():
    generate_index_social_security_info(1001, 4000)
    df = fu.read_file_to_df(corporation_index_file_url, u'年报-社保信息_index')
    df = df.fillna(0)
    fu.write_file(df, corporation_index_file_url, u'年报-社保信息_index')
    return


def generate_index_share_exchange_info(corporate_start, corporate_end):
    """
    ***年报-股东股权转让***

    指标1：变更次数，按年份，[before 2013, 2013, 2014, 2015, 2016, 2017]，总计6个，int （通过'股权变更日期'筛选而非'年报年份'）
    指标1.1：变更总次数，总计1个，int
    指标2：变更股权比例超过3%（？）的次数，[before 2013, 2013, 2014, 2015, 2016, 2017]，总计6个，int （通过'股权变更日期'筛选而非'年报年份'）
    指标2.2：变更股权比例超过3%（？）的总次数，总计1个，int
    指标3：变更股权比例超过30%（？）的次数，[before 2013, 2013, 2014, 2015, 2016, 2017]，总计6个，int （通过'股权变更日期'筛选而非'年报年份'）
    指标3.2：变更股权比例超过30%（？）的总次数，总计1个，int
    指标4：变更股权比例超过50%（？）的次数，[before 2013, 2013, 2014, 2015, 2016, 2017]，总计6个，int （通过'股权变更日期'筛选而非'年报年份'）
    指标4.2：变更股权比例超过50%（？）的总次数，总计1个，int
    指标5：变更股权比例超过80%（？）的次数，[before 2013, 2013, 2014, 2015, 2016, 2017]，总计6个，int （通过'股权变更日期'筛选而非'年报年份'）
    指标5.2：变更股权比例超过80%（？）的总次数，总计1个，int

    共计35个
    :param corporate_start:
    :param corporate_end:
    :return:
    """

    columns = ['sha_ex_count_pre_2013',
               'sha_ex_over3_count_pre_2013',
               'sha_ex_over30_count_pre_2013',
               'sha_ex_over50_count_pre_2013',
               'sha_ex_over80_count_pre_2013',
               'sha_ex_count_2013',
               'sha_ex_over3_count_2013',
               'sha_ex_over30_count_2013',
               'sha_ex_over50_count_2013',
               'sha_ex_over80_count_2013',
               'sha_ex_count_2014',
               'sha_ex_over3_count_2014',
               'sha_ex_over30_count_2014',
               'sha_ex_over50_count_2014',
               'sha_ex_over80_count_2014',
               'sha_ex_count_2015',
               'sha_ex_over3_count_2015',
               'sha_ex_over30_count_2015',
               'sha_ex_over50_count_2015',
               'sha_ex_over80_count_2015',
               'sha_ex_count_2016',
               'sha_ex_over3_count_2016',
               'sha_ex_over30_count_2016',
               'sha_ex_over50_count_2016',
               'sha_ex_over80_count_2016',
               'sha_ex_count_2017',
               'sha_ex_count_total',
               'sha_ex_over3_count_2017',
               'sha_ex_over3_count_total',
               'sha_ex_over30_count_2017',
               'sha_ex_over30_count_total',
               'sha_ex_over50_count_2017',
               'sha_ex_over50_count_total',
               'sha_ex_over80_count_2017',
               'sha_ex_over80_count_total'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-股东股权转让')
    data_frame['year'] = data_frame[u'股权变更日期'.encode('utf-8')].apply(lambda x: parser.parse(x).year)
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        for year in range(2012, 2018):
            if year == 2012:
                df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                    data_frame['year'] <= year]
            else:
                df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                    data_frame['year'] == year]

            # 变更次数
            row_list.append(len(df_temp))
            total_num1 += len(df_temp)

            if year == 2017:
                row_list.append(total_num1)
                total_num1 = 0

            # 变更股权比例超过3\30\50\80%的次数
            for ratio in [3, 30, 50, 80]:
                df_temp = df_temp[(df_temp[u'变更后股权比例'.encode('utf-8')] - df_temp[u'变更前股权比例'.encode('utf-8')]) > ratio]
                row_list.append(len(df_temp))
                if ratio == 3:
                    total_num2 += len(df_temp)
                elif ratio == 30:
                    total_num3 += len(df_temp)
                elif ratio == 50:
                    total_num4 += len(df_temp)
                elif ratio == 80:
                    total_num5 += len(df_temp)

                if year == 2017:
                    if ratio == 3:
                        row_list.append(total_num2)
                        total_num2 = 0
                    elif ratio == 30:
                        row_list.append(total_num3)
                        total_num3 = 0
                    elif ratio == 50:
                        row_list.append(total_num4)
                        total_num4 = 0
                    elif ratio == 80:
                        row_list.append(total_num5)
                        total_num5 = 0

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-股东股权转让_index', index=True)
    return


def generate_index_share_exchange_info_work():
    generate_index_share_exchange_info(1001, 4000)
    df = fu.read_file_to_df(corporation_index_file_url, u'年报-股东股权转让_index')
    df = df.fillna(0)
    fu.write_file(df, corporation_index_file_url, u'年报-股东股权转让_index')
    return


def generate_index_share_holder_info(corporate_start, corporate_end):
    """
    ***年报-股东（发起人）及出资信息_rearranged***

    指标1：股东认缴次数，按年份，[2013, 2014, 2015, 2016, 2017]，总计5个，int
    指标2：当年股东认缴出资额最大值，按年份，[2013, 2014, 2015, 2016, 2017]，总计5个，int
    指标3：当年各种方式认缴次数，按年份*认缴出资方式，[2013, 2014, 2015, 2016, 2017]*[1,2,3,4,5,6,7,8,9]，总计45个，int
    指标4：股东实缴次数，按年份，[2013, 2014, 2015, 2016, 2017]，总计5个，int
    指标5：当年股东实缴出资额最大值，按年份，[2013, 2014, 2015, 2016, 2017]，总计5个，int
    指标6：当年各种方式实缴次数，按年份*实缴出资方式，[2013, 2014, 2015, 2016, 2017]*[1,2,3,4,5,6,7,8,9]，总计45个，int
    指标7：当年认缴不等于实缴次数，按年份，[2013, 2014, 2015, 2016, 2017]，总计5个，int

    共计115个
    :param corporate_start:
    :param corporate_end:
    :return:
    """
    columns = []
    for year in range(2013, 2018):
        columns.append('sha_hol_subsc_' + str(year))
        columns.append('sha_hol_subsc_max_' + str(year))
        for category in range(1, 10):
            columns.append('sha_hol_subsc_ca' + str(category) + '_' + str(year))
        columns.append('sha_hol_confirm_' + str(year))
        columns.append('sha_hol_confirm_max_' + str(year))
        for category in range(1, 10):
            columns.append('sha_hol_confirm_ca' + str(category) + '_' + str(year))
        columns.append('sha_sub_conf_neq_' + str(year))
    print (len(columns))

    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'年报-股东（发起人）及出资信息_rearranged')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        for year in range(2013, 2018):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame[u'年报年份'.encode('utf-8')] == year]
            df_temp.loc['row_max'] = df_temp.apply(lambda x: x.max())

            # 股东认缴
            row_list.append(len(df_temp) - 1)
            row_list.append(df_temp.at['row_max', u'认缴出资额（万元）'.encode('utf-8')])
            for category in range(1, 10):
                df_cat_temp = df_temp[df_temp[u'认缴出资方式'.encode('utf-8')] == category]
                if category == 10:
                    row_list.append(len(df_cat_temp) - 1)
                else:
                    row_list.append(len(df_cat_temp))

            # 股东实缴
            row_list.append(len(df_temp) - 1)
            row_list.append(df_temp.at['row_max', u'实缴出资额（万元）'.encode('utf-8')])
            for category in range(1, 10):
                df_cat_temp = df_temp[df_temp[u'实缴出资方式'.encode('utf-8')] == category]
                if category == 10:
                    row_list.append(len(df_cat_temp) - 1)
                else:
                    row_list.append(len(df_cat_temp))

            df_temp = df_temp[df_temp[u'实缴出资额（万元）'.encode('utf-8')] != df_temp[u'认缴出资额（万元）'.encode('utf-8')]]
            row_list.append(len(df_temp))

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'年报-股东（发起人）及出资信息_index', index=True)
    return


def generate_index_share_holder_info_work():
    generate_index_share_holder_info(1001, 4000)
    df = fu.read_file_to_df(corporation_index_file_url, u'年报-股东（发起人）及出资信息_index')
    df = df.fillna(0)
    fu.write_file(df, corporation_index_file_url, u'年报-股东（发起人）及出资信息_index')
    return


soft_assets_indexes = [u'年报-企业基本信息',
                       u'年报-企业资产状况信息',
                       u'年报-对外投资信息',
                       u'年报-的对外提供保证担保信息',
                       u'年报-社保信息',
                       u'年报-股东股权转让',
                       u'年报-股东（发起人）及出资信息'
                       ]


def append_score():
    score_frame = fu.read_file_to_df(working_file_url, u'企业评分')
    score_frame = score_frame.set_index(u'企业编号'.encode('utf-8'))

    for file_n in soft_assets_indexes:
        print file_n

        data_frame = fu.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame = data_frame.set_index('Unnamed: 0')

        data_frame = data_frame.join(score_frame)

        fu.write_file(data_frame, corporation_index_file_url, file_n + '_index', index=True)
    return


def drop_score_empty():
    empty_check_list = [u'企业总评分'.encode('utf-8')]
    for file_n in soft_assets_indexes:
        print file_n

        dcu.merge_rows(file_n + '_index', file_url=corporation_index_file_url,
                       dst_file_url=corporation_index_file_url)
        dcu.drop_rows_too_many_empty(file_n + '_index', file_url=corporation_index_file_url,
                                     dst_file_url=corporation_index_file_url, columns=empty_check_list, thresh=1)
