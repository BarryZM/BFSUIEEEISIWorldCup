# *- coding:utf-8 -*-

"""
 Exploratory data utils
"""
import sys
import numpy
import file_utils
from file_directions import working_file_url, clean_data_temp_file_url, corporation_index_file_url,corporation_index_scatter_file_url
import pandas
import data_clean_utils as dcu
from files_category_info import category_finance_files
# import visualize_utils as vu


# 把面板数据变成截面数据，先建立空表
def cross_section(file_name, vars, file_url=clean_data_temp_file_url, dst_file_url=corporation_index_file_url):
    """
    指标：所有变量和时间（季度）的交叉项，转化为截面数据
    :param file_name:
    :param vars: 需要和时间交叉的变量集，写成向量
    :param empty_mask:
    :param file_url:
    :param dst_file_url:
    :return:
    """

    """
    调试函数用
    file_name=u'上市公司财务信息-每股指标'
    vars=[u'基本每股收益(元)', u'扣非每股收益(元)',u'稀释每股收益(元)',
        u'每股净资产(元)',u'每股公积金(元)',u'每股未分配利润(元)',u'每股经营现金流(元)']
    file_url = clean_data_temp_file_url
    dst_file_url = corporation_index_file_url
    """

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    date = data_frame[u'日期']  # 日期列
    unique_date = numpy.sort(list(set(date))) #删除重复，并按时间排列
    #只保留 16.9之后的
    # for j in range(0, len(unique_date)):
    #     if unique_date[j][0:3]<2016 or unique_date[j][5:6]<09:
    #         unique_date[j]=[]

    #新表的列名，是变量名和日期的交叉项
    var_date=[]
    for i in range(0,len(vars)):
        for j in range(0,len(unique_date)):
            var_date.append(vars[i]+ unique_date[j].encode('utf-8'))
    """
    尝试
    a = []
    aa=[u'每股收益',2,3]
    a = pandas.DataFrame(index=[range(1001, 3001)], columns=aa)
#   输出时文件名需要加上''，index=true表示包含第一列
    file_utils.write_file(a, file_utils.check_file_url(dst_file_url), 'a',ext='.xlsx',
                          sheet_name='Sheet', index='true')    

    ab=u'每股收益'
    ab in aa
    a.set_value(company,ab,this_number)
    
    column in var_date
    
    print data_frame.values[0][0]
    """

    # 建立空表
    b = []
    b = pandas.DataFrame(index = [range(1001,4001)],columns = var_date)

    #赋值
    for i in range(0, len(vars)):
        for j in range(0, len(data_frame)):  # 原表中的每一行
            company = data_frame.iloc[j,0]
            # at后要写列的名字，不能写列数
            # company = data_frame.at[j, u'企业总评分']
            this_season = data_frame.at[j, u'日期']
            this_number = data_frame.at[j, vars[i]]
            if this_number != 'Unknown':
                column = vars[i]+ this_season.encode('utf-8')
                b.set_value(company,column,this_number)

    file_utils.write_file(b, file_utils.check_file_url(dst_file_url), file_name+'_index', ext='.xlsx',
                      sheet_name='Sheet', index=True)

    """
    空值的处理有点问题
    status_normal = [u'--']  # 搜索满足这个条件的
    status_list = [status_normal]
    status_after = ['Unknown']  # 改成这个
    for i in range(0,len(var_date)):
        dcu.merge_status('b', u'基本每股收益(元)2010-12-31', status_list, status_after, empty_mask='-65535')
    var_date[i]
    """

    """
    运行框
        file_name=u'上市信息财务信息资产负债表'
        vars=[u'资产:货币资金(元)',u'资产:应收账款(元)',u'资产:其它应收款(元)',u'资产:存货(元)',
        u'资产:流动资产合计(元)',u'资产:长期股权投资(元)',u'资产:累计折旧(元)',u'资产:固定资产(元)',u'资产:无形资产(元)',u'资产:资产总计(元)',u'负债:应付账款(元)',
        u'负债:预收账款(元)',u'负债:存货跌价准备(元)',u'负债:流动负债合计(元)',u'负债:长期负债合计(元)',
        u'负债:负债合计(元)',u'权益:实收资本(或股本)(元)',u'权益:资本公积金(元)',u'权益:盈余公积金(元)',u'权益:股东权益合计(元)',u'流动比率']
    import exploratory_data_finance
    
    exploratory_data_finance.cross_section(u'上市公司财务信息-每股指标', [u'基本每股收益(元)', u'扣非每股收益(元)', u'稀释每股收益(元)',
                u'每股净资产(元)', u'每股公积金(元)', u'每股未分配利润(元)', u'每股经营现金流(元)'])
    exploratory_data_finance.cross_section(u'上市信息财务信息-财务风险指标', [u'资产负债率(%)',u'流动负债/总负债(%)',u'流动比率',u'速动比率'])
    exploratory_data_finance.cross_section(u'上市信息财务信息-成长能力指标', [u'营业总收入(元)',u'毛利润(元)',u'归属净利润(元)',
        u'扣非净利润(元)',u'营业总收入同比增长(元)',u'归属净利润同比增长(元)',u'扣非净利润同比增长(元)',
        u'营业总收入滚动环比增长(元)',u'归属净利润滚动环比增长(元)',u'扣非净利润滚动环比增长(元)'])
    exploratory_data_finance.cross_section(u'上市信息财务信息-利润表', [u'营业收入(元)',u'营业成本(元)',u'销售费用(元)',u'财务费用(元)',
       u'管理费用(元)',u'资产减值损失(元)',u'投资收益(元)',u'营业利润(元)',u'利润总额(元)',u'所得税(元)',u'归属母公司所有者净利润(元)'])
    exploratory_data_finance.cross_section(u'上市信息财务信息-现金流量表', [u'经营:销售商品、提供劳务收到的现金(元)',u'经营:收到的税费返还(元)',
                u'经营:收到其他与经营活动有关的现金(元)', u'经营:经营活动现金流入小计(元)',u'经营:购买商品、接受劳务支付的现金(元)',u'经营:支付给职工以及为职工支付的现金(元)',
                u'经营:支付的各项税费(元)',u'经营:支付其他与经营活动有关的现金(元)',u'经营:经营活动现金流出小计(元)',u'经营:经营活动产生的现金流量净额(元)',
                u'投资:取得投资收益所收到的现金(元)',u'投资:处置固定资产、无形资产和其他长期资产收回的现金净额(元)',u'投资:投资活动现金流入小计(元)',
                u'投资:购建固定资产、无形资产和其他长期资产支付的现金(元)',u'投资:投资支付的现金(元)',u'投资:投资活动现金流出小计(元)',
                u'投资:投资活动产生的现金流量净额(元)',u'筹资:吸收投资收到的现金(元)',u'筹资:取得借款收到的现金(元)',u'筹资:筹资活动现金流入小计(元)',
                u'筹资:偿还债务支付的现金(元)',u'筹资:分配股利、利润或偿付利息支付的现金(元)',u'筹资:筹资活动现金流出小计(元)',u'筹资活动产生的现金流量净额(元)'])

    exploratory_data_finance.cross_section(u'上市信息财务信息盈利能力指标', [u'加权净资产收益率(%)',u'摊薄净资产收益率(%)',u'摊薄总资产收益率(%)',u'毛利率(%)',u'净利率(%)',u'实际税率(%)'])
    exploratory_data_finance.cross_section(u'上市信息财务信息运营能力指标', [u'总资产周转率(次)',u'应收账款周转天数(天)',u'存货周转天数(天)'])
    exploratory_data_finance.cross_section(u'上市信息财务信息资产负债表', [u'资产:货币资金(元)',u'资产:应收账款(元)',u'资产:其它应收款(元)',u'资产:存货(元)',
        u'资产:流动资产合计(元)',u'资产:长期股权投资(元)',u'资产:累计折旧(元)',u'资产:固定资产(元)',u'资产:无形资产(元)',u'资产:资产总计(元)',u'负债:应付账款(元)',
        u'负债:预收账款(元)',u'负债:存货跌价准备(元)',u'负债:流动负债合计(元)',u'负债:长期负债合计(元)',
        u'负债:负债合计(元)',u'权益:实收资本(或股本)(元)',u'权益:资本公积金(元)',u'权益:盈余公积金(元)',u'权益:股东权益合计(元)',u'流动比率'])

    """
    return

def drop_indexes_too_many_empty(): #删空行太多的列。已经跑过一遍这个函数的表再跑会加一列序号
    for file_n in category_finance_files:
        df = file_utils.read_file_to_df(corporation_index_file_url, file_n + '_index')
        df = df.dropna(axis=1, thresh=1000)
        df = df.fillna(-65535)  # empty value is filled with -65535
        file_utils.write_file(df, corporation_index_file_url, file_n + '_index')


def append_score(): #加上评分
    """
        append score to each index file.
        :return:
        """
    score_frame = file_utils.read_file_to_df(working_file_url, u'企业评分')
    score_frame = score_frame.set_index(u'企业编号')

    for file_n in category_finance_files:
        print file_n
        data_frame = file_utils.read_file_to_df(corporation_index_file_url, file_n + '_index')
        # columns = data_frame.columns.values.tolist()
        # print data_frame
        try:
            data_frame = data_frame.set_index('Unnamed: 0')
        except KeyError, f:
            print f.message
        try:
            data_frame = data_frame.join(score_frame)
            file_utils.write_file(data_frame, corporation_index_file_url, file_n + '_index', index=True)
        except ValueError,e:
            print e.message

    return


def drop_score_empty(): #删去评分为空的公式，如果第一列名为空，第一列也会被删
    """
    some corporates lack of scores, we need to drop them.
    :return:
    """
    empty_check_list = [u'企业总评分']
    for file_n in category_finance_files:
        print file_n

        dcu.merge_rows(file_n + '_index', file_url=corporation_index_file_url,
                       dst_file_url=corporation_index_file_url)
        dcu.drop_rows_too_many_empty(file_n + '_index', file_url=corporation_index_file_url,
                                     dst_file_url=corporation_index_file_url, columns=empty_check_list, thresh=1)


def score_integerize(): # 评分化为整数
    """
    scores are float, and we want try if integers will helps.
    :return:
    """
    for file_n in category_finance_files:
        print file_n

        data_frame = file_utils.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame['int_score'] = data_frame[u'企业总评分'].apply(lambda x: round(x))

        file_utils.write_file(data_frame, corporation_index_file_url, file_n + '_index')


def pic_scatter():
    """
    plot scatter pictures for each index and score.
    :return:
    """
    print category_finance_files
    # vu.pic_scatter(category_finance_files, 'finance')




