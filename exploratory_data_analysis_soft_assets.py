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
import pandas as pd
from dateutil import parser

import data_clean_utils as dcu
import exploratory_data_utils as edu
import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url, corporate_index_false, \
    corporate_index_true, working_file_url
import visualize_utils as vu


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


def generate_index_work(corporate_start, corporate_end):
    """
    ***作品著作权***
    指标1：作品著作权个数，总计1个，int
    指标2：近1年作品著作权个数，总计1个，int
    指标3：近3年作品著作权个数，总计1个，int
    指标4：分类别作品著作权个数，总计9个，int

    总计12个
    :return:
    """
    columns = ['works_total',
               'works_2018',
               'works_2016_2019',
               'works_1',
               'works_2',
               'works_3',
               'works_4',
               'works_5',
               'works_6',
               'works_7',
               'works_8',
               'works_9'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'作品著作权')
    data_frame['year'] = data_frame[u'作品著作权登记日期'.encode('utf-8')].apply(
        lambda x: edu.cal_year_in_work_copyright(x))

    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        df_temp = data_frame[data_frame[corporate_index_false] == corporate]

        # 作品著作权个数
        row_list.append(len(df_temp))

        # 作品著作权个数2018
        df_y_temp = df_temp[df_temp['year'] == 2018]
        row_list.append(len(df_y_temp))

        # 作品著作权个数2016-2019
        df_y_temp = df_temp[df_temp['year'] >= 2016]
        row_list.append(len(df_y_temp))

        # 分类别作品著作权个数
        for category in range(1, 10):
            df_c_temp = df_temp[df_temp[u'作品著作权类别'.encode('utf-8')] == category]
            row_list.append(len(df_c_temp))

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'作品著作权_index', index=True)
    return


def generate_index_work_work():
    generate_index_work(1001, 4000)
    return


def generate_index_trademark(corporate_start, corporate_end):
    """
    ***商标***
    指标1：商标总个数，总计1个，int
    指标2：分状态商标数，总计8个，int
    指标9：1993（含）年前申请商标个数，总计1个，int
    指标10：2000（含）年前申请商标个数，总计1个，int
    指标11：2010（含）年前申请商标个数，总计1个，int
    指标12：2017-2018年申请商标个数，总计1个，int
    指标13：2016-2018年申请商标商标已注册状态商标个数，总计1个，int
    指标14：商标使用期限时间段超过2019-01-01（含）商标个数，总计1个，int
    指标15：商标使用期限时间段超过2024-01-01（含）商标个数，总计1个，int
    指标16：商标使用期限时间段超过2029-01-01（含）商标个数，总计1个，int

    总计17个

    :return:
    """
    columns = ['tra_mark_total',
               'tra_mark_0',
               'tra_mark_1',
               'tra_mark_2',
               'tra_mark_3',
               'tra_mark_4',
               'tra_mark_5',
               'tra_mark_6',
               'tra_mark_7',
               'tra_mark_pre_1993',
               'tra_mark_pre_2000',
               'tra_mark_pre_2010',
               'tra_mark_apply_2017_2018',
               'tra_mark_reg_2016_2018',
               'tra_mark_over_2019',
               'tra_mark_over_2024',
               'tra_mark_over_2029'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'商标')
    data_frame['year_to'] = data_frame[u'商标使用期限时间段'.encode('utf-8')].apply(
        lambda x: edu.cal_year_in_trademark(x))
    data_frame['year_apply'] = data_frame[u'申请日期'.encode('utf-8')].apply(
        lambda x: parser.parse(x).year)

    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        df_temp = data_frame[data_frame[corporate_index_false] == corporate]

        # 商标总个数
        row_list.append(len(df_temp))

        # 分状态商标数
        for category in range(0, 8):
            df_c_temp = df_temp[df_temp[u'商标状态'.encode('utf-8')] == category]
            row_list.append(len(df_c_temp))

        df_y_tal_temp = df_temp[df_temp['year_apply'] > 1000]
        # 1993（含）年前申请商标个数
        df_y_temp = df_y_tal_temp[df_y_tal_temp['year_apply'] <= 1993]
        row_list.append(len(df_y_temp))

        # 2000（含）年前申请商标个数
        df_y_temp = df_y_tal_temp[df_y_tal_temp['year_apply'] <= 2000]
        row_list.append(len(df_y_temp))

        # 2010（含）年前申请商标个数
        df_y_temp = df_y_tal_temp[df_y_tal_temp['year_apply'] <= 2010]
        row_list.append(len(df_y_temp))

        # 2017-2018年申请商标个数
        df_y_temp = df_y_tal_temp[df_y_tal_temp['year_apply'] >= 2017][df_y_tal_temp['year_apply'] <= 2018]
        row_list.append(len(df_y_temp))

        # 2016-2018年申请商标商标已注册状态商标个数
        df_y_temp = df_y_tal_temp[df_y_tal_temp['year_apply'] >= 2016][df_y_tal_temp['year_apply'] <= 2018][
            df_temp[u'商标状态'.encode('utf-8')] < 1]
        row_list.append(len(df_y_temp))

        # 商标使用期限时间段超过2019-01-01（含）商标个数
        df_y_temp = df_y_tal_temp[df_y_tal_temp['year_to'] >= 2019]
        row_list.append(len(df_y_temp))

        # 商标使用期限时间段超过2024-01-01（含）商标个数
        df_y_temp = df_y_temp[df_y_temp['year_to'] >= 2024]
        row_list.append(len(df_y_temp))

        # 商标使用期限时间段超过2029-01-01（含）商标个数
        df_y_temp = df_y_temp[df_y_temp['year_to'] >= 2029]
        row_list.append(len(df_y_temp))

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'商标_index', index=True)
    return


def generate_index_trademark_work():
    generate_index_trademark(1001, 4000)
    return


def generate_index_certificate(corporate_start, corporate_end):
    """
    ***资质认证***
    指标1：资质认证总个数，总计1个，int
    指标1.1：资质认证种类数，总计1个，int
    指标1.2：有效资质认证种类数，总计1个，int
    指标2：有效期截至日期在2019-01-01（含）之后的个数，总计1个，int
    指标3：有效期截至日期在2023-01-01（含）之后的个数，总计1个，int
    指标4：有效期截至日期在2024-01-01（含）之后的个数，总计1个，int
    指标5：有效期起止日期在2011-01-01（不含）之前的个数，总计1个，int
    指标6：有效期起止日期在2006-01-01（不含）之前的个数，总计1个，int
    指标7：各状态资质认证个数，总计3个，int
    指标8：各种类资质数，总计7个，int

    总计19个

    :return:
    """
    columns = ['certi_total',
               'certi_cat_total',
               'certi_valid_cat_total',
               'certi_after_2019',
               'certi_after_2023',
               'certi_after_2024',
               'certi_before_2011',
               'certi_before_2006',
               'certi_valid',
               'certi_invalid',
               'certi_sta_unkw',
               'certi_cat_0',
               'certi_cat_1',
               'certi_cat_2',
               'certi_cat_3',
               'certi_cat_4',
               'certi_cat_5',
               'certi_cat_6',
               'certi_cat_7'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'资质认证')
    data_frame['start_year'] = data_frame[u'有效期起止日期'.encode('utf-8')].apply(
        lambda x: edu.cal_year_in_common(x))
    data_frame['end_year'] = data_frame[u'有效期截至日期'.encode('utf-8')].apply(
        lambda x: edu.cal_year_in_common(x))

    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        df_temp = data_frame[data_frame[corporate_index_false] == corporate]

        # 资质认证总个数
        row_list.append(len(df_temp))

        # 资质认证种类数
        value = df_temp.nunique().get(u'证书名称'.encode('utf-8'))
        if not isinstance(value, int):
            value = 0
        row_list.append(value)

        # 有效资质认证种类数
        df_s_temp = df_temp[df_temp[u'状态'.encode('utf-8')] == 0]
        value = df_s_temp.nunique().get(u'证书名称'.encode('utf-8'))
        if not isinstance(value, int):
            value = 0
        row_list.append(value)

        # 有效期截至日期在2019-01-01（含）之后的个数
        df_y_temp = df_temp[df_temp['end_year'] >= 2019]
        row_list.append(len(df_y_temp))

        # 有效期截至日期在2023-01-01（含）之后的个数
        df_y_temp = df_y_temp[df_y_temp['end_year'] >= 2023]
        row_list.append(len(df_y_temp))

        # 有效期截至日期在2024-01-01（含）之后的个数
        df_y_temp = df_y_temp[df_y_temp['end_year'] >= 2024]
        row_list.append(len(df_y_temp))

        # 有效期起止日期在2011-01-01（不含）之前的个数
        df_y_temp = df_temp[df_temp['start_year'] < 2011][df_temp['start_year'] > 1000]
        row_list.append(len(df_y_temp))

        # 有效期起止日期在2006-01-01（不含）之前的个数
        df_y_temp = df_y_temp[df_y_temp['start_year'] < 2006]
        row_list.append(len(df_y_temp))

        # 各状态资质认证个数
        for status in range(0, 3):
            df_s_temp = df_temp[df_temp[u'状态'.encode('utf-8')] == status]
            row_list.append(len(df_s_temp))

        # 各种类资质认证个数
        for category in range(0, 8):
            df_c_temp = df_temp[df_temp[u'categories'] == category]
            row_list.append(len(df_c_temp))

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'资质认证_index', index=True)
    return


def generate_index_certificate_work():
    generate_index_certificate(1001, 4000)
    return


def generate_index_copyright(corporate_start, corporate_end):
    """
    ***软著著作权***
    指标1：软件著作权个数，总计1个，int
    指标2：软件著作权登记批准日期在2017-01-01（含）之后的个数，总计1个，int
    指标3：软件著作权登记批准日期在2013-01-01（不含）之前的个数，总计1个，int
    指标4：软件著作权登记批准日期在2006-01-01（不含）之前的个数，总计1个，int

    总计4个
    :return:
    """
    columns = ['copyright_total',
               'copyright_after_2017',
               'copyright_before_2013',
               'copyright_before_2006'
               ]
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'软著著作权')
    data_frame['year'] = data_frame[u'软件著作权登记批准日期'.encode('utf-8')].apply(
        lambda x: edu.cal_year_in_common(x))

    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        df_temp = data_frame[data_frame[corporate_index_false] == corporate]

        # 软件著作权个数
        row_list.append(len(df_temp))

        # 软件著作权登记批准日期在2017-01-01（含）之后的个数
        df_y_temp = df_temp[df_temp['year'] >= 2017]
        row_list.append(len(df_y_temp))

        # 软件著作权登记批准日期在2013-01-01（不含）之前的个数
        df_y_temp = df_temp[df_temp['year'] < 2013][df_temp['year'] > 1000]
        row_list.append(len(df_y_temp))

        # 软件著作权登记批准日期在2006-01-01（不含）之前的个数
        df_y_temp = df_y_temp[df_y_temp['year'] < 2006]
        row_list.append(len(df_y_temp))

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'软著著作权_index', index=True)
    return


def generate_index_copyright_work():
    generate_index_copyright(1001, 4000)
    return


def generate_index_program(corporate_start, corporate_end):
    """
    ***项目信息***
    指标1：项目个数，总计1个，int
    指标2：2010-01-01（含）后项目个数，总计1个，int
    指标3：项目行业数，总计1个，int
    指标4：项目行业，总计5个（如果项目行业只有1个，则co_industry_1为其行业，其余为0），int

    总计2个
    :return:
    """
    columns = ['program_total',
               'program_industries',
               'program_after_2010',
               'co_industry_1',
               'co_industry_2',
               'co_industry_3',
               'co_industry_4',
               'co_industry_5'
               ]
    dis_df = pd.DataFrame(columns=columns)

    industry_frame = fu.read_file_to_df(clean_data_temp_file_url, 'industry')

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'项目信息')
    data_frame['year'] = data_frame[u'项目成立时间'.encode('utf-8')].apply(
        lambda x: edu.cal_year_in_common(x))

    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        df_temp = data_frame[data_frame[corporate_index_false] == corporate]
        df_temp = df_temp.reset_index()

        # 项目个数
        row_list.append(len(df_temp))

        industry_count = df_temp.nunique().get('industry')
        if not isinstance(industry_count, int):
            industry_count = 0
        row_list.append(industry_count)
        if industry_count > 1:
            print df_temp
            print '--------------------'

        # 2010-01-01（含）后项目个数
        df_y_temp = df_temp[df_temp['year'] >= 2010]
        row_list.append(len(df_y_temp))

        # 项目行业
        for i in range(1, 6):
            isadded = False
            if len(df_temp) >= i:
                for j in range(1, industry_frame.shape[1] + 1):
                    if df_temp.at[i - 1, 'industry'] in industry_frame[j].to_list():
                        row_list.append(j)
                        isadded = True
                        break
            if not isadded:
                row_list.append(0)

        row_dict[corporate] = row_list
        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'项目信息_index', index=True)
    return


def generate_index_program_work():
    generate_index_program(1001, 4000)
    return


soft_assets_indexes = [u'专利',
                       u'产品',
                       u'作品著作权',
                       u'商标',
                       u'资质认证',
                       u'软著著作权',
                       u'项目信息'
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


def score_integerize():
    for file_n in soft_assets_indexes:
        print file_n

        data_frame = fu.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame['int_score'] = data_frame[u'企业总评分'.encode('utf-8')].apply(lambda x: round(x))

        fu.write_file(data_frame, corporation_index_file_url, file_n + '_index')


def pic_scatter():
    vu.pic_scatter(soft_assets_indexes, 'soft_assets')
