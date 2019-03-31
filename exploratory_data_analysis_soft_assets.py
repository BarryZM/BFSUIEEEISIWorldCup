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
from file_directions import clean_data_temp_file_url, corporation_index_file_url, corporate_index_false, \
    corporate_index_true
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
    status_1 = [u'发明专利', u'发明公布', u'发明公布更正', u'发明授权', u'发明授权更正']
    status_2 = [u'外观设计', u'外观设计更正']
    status_3 = [u'实用新型', u'实用新型更正']
    status_list = [status_1, status_2, status_3]
    status_after = [0, 1, 2]
    dcu.merge_status(u'专利', u'专利类型'.encode('utf-8'), status_list, status_after)

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

    # numeric first
    # registered
    status_1 = [u'商标已注册',
                u'出具商标注册证明中',
                u'出具商标注册证明完成',
                u'排版送达公告(商标注册证)',
                u'排版送达公告(商标注册证商品服务附页)',
                u'排版送达公告(商标注册证明)',
                u'排版送达公告(商标续展注册证明)',
                u'排版送达公告(补发注册证领证通知书)',
                u'排版送达公告(领取商标注册证通知书)'
                ]
    status_2 = [u'核准证明打印发送',
                u'核准通知书打印发送',
                u'核准通知打印发送',
                u'等待注册公告公示期',
                u'等待注册发文',
                u'等待结案通知书发文',
                u'等待继续有效通知发文',
                u'许可合同备案完成',
                u'许可合同备案待审中',
                u'评审分案'
                ]
    status_3 = [u'注册',
                u'注册申请初步审定',
                u'注册申请部分驳回',
                u'注册证发文',
                u'排版注册公告',
                u'申请收文',
                u'商标注册申请中',
                u'商标注册申请受理通知书',
                u'商标注册申请受理通知书发文',
                u'商标注册申请注册公告排版完成',
                u'商标注册申请等待受理中',
                u'商标注册申请等待受理通知书发文',
                u'商标注册申请等待驳回复审',
                u'商标注册申请等待驳回通知发文',
                u'商标注册申请驳回通知发文',
                u'商标注册申请注册公告排版完成',
                u'商标注册申请完成',
                u'商标使用许可备案中',
                u'商标使用许可备案完成',
                u'初步审定公告',
                u'等待受理通知书发文',
                u'等待受理通知发文',
                u'等待实审裁文发文',
                u'等待实质审查',
                u'等待审查意见书发文',
                u'等待意见书回文',
                u'等待打印受理通知',
                u'等待打印受理通知书',
                u'等待打印注册证',
                u'等待抽签发文',
                u'等待提供证明通知发文',
                ]
    status_4 = [u'驳回复审不予受理',
                u'驳回复审中',
                u'驳回复审完成',
                u'驳回复审待审中',
                u'驳回复审排版送达公告(初步审定公告通知书)',
                u'驳回复审排版送达公告(商标注册证)',
                u'驳回复审排版送达公告(商标评审申请受理通知书)',
                u'驳回复审排版送达公告(驳回复审决定书)',
                u'驳回复审有退信(商标评审申请受理通知书)',
                u'驳回复审有退信(领取商标注册证通知书)',
                u'驳回复审注册公告排版完成',
                u'驳回复审评审实审裁文发文',
                u'驳回复审评审实审裁文等待实审裁文发文',
                u'驳回复审评审形审不予受理通知发文',
                u'驳回复审评审形审视为撤回发文',
                u'驳回复审领退信(商标评审申请受理通知书)',
                u'驳回复审领退信(驳回复审决定书)',
                u'驳回转让完成',
                u'驳回通知发文'
                ]
    status_5 = [u'商标无效',
                u'变更视为放弃',
                u'冻结商标中',
                u'冻结商标完成',
                u'无效宣告中',
                u'无效宣告完成',
                u'无效宣告排版送达公告(商标无效宣告答辩通知书)',
                u'无效宣告排版送达公告(商标评审申请受理通知书)',
                u'无效宣告排版送达公告(无效宣告请求裁定书)',
                u'无效宣告有退信(无效宣告请求裁定书)',
                u'无效宣告评审实审裁文发文',
                u'无效宣告领退信(商标无效宣告答辩通知书)'
                ]
    status_6 = [u'商标续展中',
                u'商标续展完成',
                u'商标续展待审中',
                ]
    status_7 = [u'商标转让中',
                u'商标转让完成',
                ]

    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7]
    status_after = [0, 1, 2, 3, 4, 5, 6, 7]
    # dcu.merge_status(u'商标', u'商标状态'.encode('utf-8'), status_list, status_after, others=8)

    columns = ['tra_mark_total',
               'tra_mark_1',
               'tra_mark_2',
               'tra_mark_3',
               'tra_mark_4',
               'tra_mark_5',
               'tra_mark_6',
               'tra_mark_7',
               'tra_mark_8',
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
        for category in range(1, 9):
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
