# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis)
"""




import file_utils as fu
from file_directions import clean_data_temp_file_url, corporation_index_file_url,  working_file_url
import pandas as pd
from files_category_info import category_landing_purchase
import visualize_utils as vu
import exploratory_data_utils as edu
import data_clean_utils as dcu


def generate_index_gddkgs(corporate_start, corporate_end):

    """
    ***购地-地块公示***
    指标1：公司总购地数，总计1个，int
    指标2：公司购地总面积，总计1个，int
    指标3：公司不同土地用途购地数量，总计8个，int
    指标4：公司近5年购地次数，总计1个，int
    指标5：公司自2008年至2018年每年的购地数，总计11个，int
    指标6：公司自2008年至2018年每年的购地面积，总计11个，int
    :return:
    """



    columns = ['landing_purchasing_count',
               'landing_acre_count',
               'status_5',
               'status_6',
               'status_7',
               'status_8',
               'status_9',
               'status_10',
               'status_11',
               'status_12',
               'landing_purchase_in_last_5_years',
               'landing_purchasing_count_2008',
               'landing_purchasing_count_2009',
               'landing_purchasing_count_2010',
               'landing_purchasing_count_2011',
               'landing_purchasing_count_2012',
               'landing_purchasing_count_2013',
               'landing_purchasing_count_2014',
               'landing_purchasing_count_2015',
               'landing_purchasing_count_2016',
               'landing_purchasing_count_2017',
               'landing_purchasing_count_2018',
               'landing_acre_count_2008',
               'landing_acre_count_2009',
               'landing_acre_count_2010',
               'landing_acre_count_2011',
               'landing_acre_count_2012',
               'landing_acre_count_2013',
               'landing_acre_count_2014',
               'landing_acre_count_2015',
               'landing_acre_count_2016',
               'landing_acre_count_2017',
               'landing_acre_count_2018']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'购地-地块公示')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]

        # 公司总购地数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 公司购地总面积
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'土地面积（公顷）'.encode('utf-8')]
        row_list.append(amount)
        total_num2 += amount

        # 公司不同土地用途购地数量
        for status in range(1,9):
            y_df = df_temp.loc[df_temp[u'土地用途'.encode('utf-8')] == status]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)


        # 公司近5年购地次数
        y_df = df_temp.loc[(df_temp['year0'] > 2013) & (df_temp['year0'] <=2019)]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)


        for year in range(2008,2019):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame['year0'] == year]


            # 公司自2008年至2018年每年的购地数
            row_list.append(len(df_temp))
            total_num5 += len(df_temp)

            # 公司自2008年至2018年每年的购地面积
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'土地面积（公顷）'.encode('utf-8')]
            row_list.append(amount)
            total_num6 += amount

        row_dict[corporate] = row_list

        dis_df = dis_df.fillna({'landing_purchasing_count_2008': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2009': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2010': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2011': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2012': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2013': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2014': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2015': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2016': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2017': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2018': 0})

        dis_df = dis_df.fillna({'landing_acre_count': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2008': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2009': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2010': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2011': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2012': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2013': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2014': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2015': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2016': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2017': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2018': 0})

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'购地-地块公示_index', index=True)
    return



def generate_index_gdscjytddy(corporate_start, corporate_end):

    """
    ***购地-市场交易-土地抵押***
    指标1：公司抵押次数，总计1个，int
    指标2：公司抵押总面积，总计1个，int
    指标3：公司不同土地用途数量，总计8个，int
    指标4：公司不同土地用途抵押数量，总计8个，int
    指标5：公司不同抵押土地使用权属性数量，总计3个，int
    指标6：公司抵押土地评估金额，总计1个，int
    指标7：公司抵押土地金额，总计1个，int
    指标8：公司近5年抵押次数，总计1个，int
    指标9：公司2008-2018每年抵押次数，总计11个，int
    指标10：公司2008-2018每年抵押面积，总计11个，int
    指标11：公司2008-2018每年抵押土地金额，总计11个，int
    指标12：公司2019-2021每年到期抵押次数，总计3个，int
    指标13：公司2019-2021每年到期抵押面积，总计3个，int
    指标14：公司2019-2021每年到期抵押土地金额，总计3个，int
    :return:
    """



    columns = ['landing_mortgage_count',
               'landing_acre_count',
               'landing_mortgage_acre_count',
               'status_5',
               'status_6',
               'status_7',
               'status_8',
               'status_9',
               'status_10',
               'status_11',
               'status_12',
               'status_mortgage_5',
               'status_mortgage_6',
               'status_mortgage_7',
               'status_mortgage_8',
               'status_mortgage_9',
               'status_mortgage_10',
               'status_mortgage_11',
               'status_mortgage_12',
               'usage rights_1',
               'usage rights_2',
               'usage rights_3',
               'assessment_value_of_mortgaged_land',
               'real_value_of_mortgaged_land',
               'mortgage_in_last_5_years',
               'landing_mortgage_count_2008',
               'landing_mortgage_count_2009',
               'landing_mortgage_count_2010',
               'landing_mortgage_count_2011',
               'landing_mortgage_count_2012',
               'landing_mortgage_count_2013',
               'landing_mortgage_count_2014',
               'landing_mortgage_count_2015',
               'landing_mortgage_count_2016',
               'landing_mortgage_count_2017',
               'landing_mortgage_count_2018',
               'landing_mortgage_acre_count_2008',
               'landing_mortgage_acre_count_2009',
               'landing_mortgage_acre_count_2010',
               'landing_mortgage_acre_count_2011',
               'landing_mortgage_acre_count_2012',
               'landing_mortgage_acre_count_2013',
               'landing_mortgage_acre_count_2014',
               'landing_mortgage_acre_count_2015',
               'landing_mortgage_acre_count_2016',
               'landing_mortgage_acre_count_2017',
               'landing_mortgage_acre_count_2018',
               'real_value_of_mortgaged_land_2008',
               'real_value_of_mortgaged_land_2009',
               'real_value_of_mortgaged_land_2010',
               'real_value_of_mortgaged_land_2011',
               'real_value_of_mortgaged_land_2012',
               'real_value_of_mortgaged_land_2013',
               'real_value_of_mortgaged_land_2014',
               'real_value_of_mortgaged_land_2015',
               'real_value_of_mortgaged_land_2016',
               'real_value_of_mortgaged_land_2017',
               'real_value_of_mortgaged_land_2018',
               'landing_mortgage_count_2019',
               'landing_mortgage_count_2020',
               'landing_mortgage_count_2021',
               'landing_mortgage_acre_count_2019',
               'landing_mortgage_acre_count_2020',
               'landing_mortgage_acre_count_2021',
               'real_value_of_mortgaged_land_2019',
               'real_value_of_mortgaged_land_2020',
               'real_value_of_mortgaged_land_2021']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'购地-市场交易-土地抵押')
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
        total_num9 = 0
        total_num10 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]

        # 公司总抵押地数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 公司土地面积
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'土地面积'.encode('utf-8')]
        row_list.append(amount)
        total_num2 += amount

        # 公司抵押土地面积
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'抵押面积(公顷)'.encode('utf-8')]
        row_list.append(amount)
        total_num3 += amount

        # 公司不同土地用途数量
        for status in range(1, 9):
            y_df = df_temp.loc[df_temp[u'土地用途'.encode('utf-8')] == status]
            row_list.append(len(y_df))
            total_num4 += len(df_temp)

        # 公司不同土地用途抵押数量
        for status in range(1, 9):
            y_df = df_temp.loc[df_temp[u'抵押土地用途'.encode('utf-8')] == status]
            row_list.append(len(y_df))
            total_num5 += len(df_temp)

        # 抵押土地使用权属性
        for i in range(1, 4):
            y_df = df_temp.loc[df_temp[u'抵押土地权属性质与使用权类型'.encode('utf-8')] == i]
            row_list.append(len(y_df))
            total_num6 += len(df_temp)

        # 公司抵押土地评估金额
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'评估金额(万元)'.encode('utf-8')]
        row_list.append(amount)
        total_num7 += amount

        # 公司抵押土地金额
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'抵押金额(万元)'.encode('utf-8')]
        row_list.append(amount)
        total_num8 += amount

        # 公司近5年抵押土地次数
        y_df = df_temp.loc[(df_temp['year0'] > 2013) & (df_temp['year0'] <= 2019)]
        row_list.append(len(y_df))
        total_num9 += len(df_temp)

        for year in range(2008,2019):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame['year0'] == year]

            # 公司2008年-2018年抵押地数
            row_list.append(len(df_temp))
            total_num1 += len(df_temp)

            # 公司2008年-2018年抵押土地面积
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'抵押面积(公顷)'.encode('utf-8')]
            row_list.append(amount)
            total_num3 += amount

            # 公司抵押土地金额
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'抵押金额(万元)'.encode('utf-8')]
            row_list.append(amount)
            total_num8 += amount


        for year in range(2019,2022):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame['year1'] == year]

            # 公司2019年-2021年抵押期满土地数
            row_list.append(len(df_temp))
            total_num1 += len(df_temp)

            # 公司22019年-2021年抵押期满土地面积
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'抵押面积(公顷)'.encode('utf-8')]
            row_list.append(amount)
            total_num3 += amount

            # 公司2019年-2021年抵押期满土地金额
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'抵押金额(万元)'.encode('utf-8')]
            row_list.append(amount)
            total_num8 += amount

        row_dict[corporate] = row_list

        # 对空值进行处理以进行索引
        dis_df = dis_df.fillna({'landing_mortgage_count_2008': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2009': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2010': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2011': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2012': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2013': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2014': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2015': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2016': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2017': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2018': 0})

        dis_df = dis_df.fillna({'landing_acre_count': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2008': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2009': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2010': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2011': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2012': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2013': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2014': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2015': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2016': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2017': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2018': 0})

        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2008': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2009': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2010': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2011': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2012': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2013': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2014': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2015': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2016': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2017': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2018': 0})

        dis_df = dis_df.fillna({'landing_mortgage_count_2019': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2020': 0})
        dis_df = dis_df.fillna({'landing_mortgage_count_2021': 0})

        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2019': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2020': 0})
        dis_df = dis_df.fillna({'landing_mortgage_acre_count_2021': 0})

        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2019': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2020': 0})
        dis_df = dis_df.fillna({'real_value_of_mortgaged_land_2021': 0})

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'购地-市场交易-土地抵押_index', index=True)
    return



def generate_index_gdscjytdzr(corporate_start, corporate_end):

    """
    ***购地-市场交易-土地转让***
    指标1：公司总土地转让数，总计1个，int
    指标2：公司总土地转让数，总计1个，int
    指标3：公司不同土地用途转让数量，总计8个，int
    指标4：公司近5年转让次数，总计1个，int
    指标5：公司自2008年至2018年每年的转让数，总计11个，int
    指标6：公司自2008年至2018年每年的转让面积，总计11个，int
    :return:
    """



    columns = ['landing_transfer_count',
               'landing_transfer_acre_count',
               'status_transfer_5',
               'status_transfer_6',
               'status_transfer_7',
               'status_transfer_8',
               'status_transfer_9',
               'status_transfer_10',
               'status_transfer_11',
               'status_transfer_12',
               'landing_transfer_in_last_5_years',
               'landing_transfer_count_2008',
               'landing_transfer_count_2009',
               'landing_transfer_count_2010',
               'landing_transfer_count_2011',
               'landing_transfer_count_2012',
               'landing_transfer_count_2013',
               'landing_transfer_count_2014',
               'landing_transfer_count_2015',
               'landing_transfer_count_2016',
               'landing_transfer_count_2017',
               'landing_transfer_count_2018',
               'landing_transfer_acre_count_2008',
               'landing_transfer_acre_count_2009',
               'landing_transfer_acre_count_2010',
               'landing_transfer_acre_count_2011',
               'landing_transfer_acre_count_2012',
               'landing_transfer_acre_count_2013',
               'landing_transfer_acre_count_2014',
               'landing_transfer_acre_count_2015',
               'landing_transfer_acre_count_2016',
               'landing_transfer_acre_count_2017',
               'landing_transfer_acre_count_2018']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'购地-市场交易-土地转让')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]

        # 公司总土地转让数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 公司土地转让总面积
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'土地面积(公顷)'.encode('utf-8')]
        row_list.append(amount)
        total_num2 += amount

        # 公司不同土地用途转让数量
        for status in range(1,9):
            y_df = df_temp.loc[df_temp[u'土地用途'.encode('utf-8')] == status]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)


        # 公司近5年转让次数
        y_df = df_temp.loc[(df_temp['year0'] > 2013) & (df_temp['year0'] <=2019)]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)


        for year in range(2008,2019):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame['year0'] == year]


            # 公司自2008年至2018年每年的转让数
            row_list.append(len(df_temp))
            total_num5 += len(df_temp)

            # 公司自2008年至2018年每年的转让面积
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'土地面积(公顷)'.encode('utf-8')]
            row_list.append(amount)
            total_num6 += amount

        row_dict[corporate] = row_list

        # 对空值进行处理以进行索引
        dis_df = dis_df.fillna({'landing_transfer_count_2008': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2009': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2010': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2011': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2012': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2013': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2014': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2015': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2016': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2017': 0})
        dis_df = dis_df.fillna({'landing_transfer_count_2018': 0})

        dis_df = dis_df.fillna({'landing_transfer_acre_count': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2008': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2009': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2010': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2011': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2012': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2013': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2014': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2015': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2016': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2017': 0})
        dis_df = dis_df.fillna({'landing_transfer_acre_count_2018': 0})

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'购地-市场交易-土地转让_index', index=True)
    return



def generate_index_fdcdqygdqk(corporate_start, corporate_end):

    """
    ***购地-房地产大企业购地情况***
    指标1：房地产公司供地总次数，总计1个，int
    指标2：房地产公司供地总面积，总计1个，int
    指标3：房地产公司不同土地用途供地数量，总计8个，int
    指标4：公司近5年供地总次数，总计1个，int
    指标5：房地产公司自2008年至2018年每年供地次数，总计11个，int
    指标6：房地产公司自2008年至2018年每年的供地面积，总计11个，int
    :return:
    """



    columns = ['house_landing_supply_count',
               'house_landing_supply_acre_count',
               'house_supply_status_5',
               'house_supply_status_6',
               'house_supply_status_7',
               'house_supply_status_8',
               'house_supply_status_9',
               'house_supply_status_10',
               'house_supply_status_11',
               'house_supply_status_12',
               'house_landing_supply_in_last_5_years',
               'house_landing_supply_count_2008',
               'house_landing_supply_count_2009',
               'house_landing_supply_count_2010',
               'house_landing_supply_count_2011',
               'house_landing_supply_count_2012',
               'house_landing_supply_count_2013',
               'house_landing_supply_count_2014',
               'house_landing_supply_count_2015',
               'house_landing_supply_count_2016',
               'house_landing_supply_count_2017',
               'house_landing_supply_count_2018',
               'house_landing_supply_acre_count_2008',
               'house_landing_supply_acre_count_2009',
               'house_landing_supply_acre_count_2010',
               'house_landing_supply_acre_count_2011',
               'house_landing_supply_acre_count_2012',
               'house_landing_supply_acre_count_2013',
               'house_landing_supply_acre_count_2014',
               'house_landing_supply_acre_count_2015',
               'house_landing_supply_acre_count_2016',
               'house_landing_supply_acre_count_2017',
               'house_landing_supply_acre_count_2018']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'购地-房地产大企业购地情况')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]

        # 房地产公司供地总次数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 房地产公司供地总面积
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'供地总面积（公顷）'.encode('utf-8')]
        row_list.append(amount)
        total_num2 += amount

        # 房地产公司不同土地用途供地数量
        for status in range(1,9):
            y_df = df_temp.loc[df_temp[u'土地用途'.encode('utf-8')] == status]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)


        # 公司近5年供地总次数
        y_df = df_temp.loc[(df_temp['year0'] > 2013) & (df_temp['year0'] <=2019)]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)


        for year in range(2008,2019):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame['year0'] == year]


            # 房地产公司自2008年至2018年每年供地次数
            row_list.append(len(df_temp))
            total_num5 += len(df_temp)

            # 房地产公司自2008年至2018年每年的供地面积
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'供地总面积（公顷）'.encode('utf-8')]
            row_list.append(amount)
            total_num6 += amount

        row_dict[corporate] = row_list

        # 对空值进行处理以进行索引
        dis_df = dis_df.fillna({'house_landing_supply_count_2008': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2009': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2010': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2011': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2012': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2013': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2014': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2015': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2016': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2017': 0})
        dis_df = dis_df.fillna({'house_landing_supply_count_2018': 0})

        dis_df = dis_df.fillna({'house_landing_supply_acre_count': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2008': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2009': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2010': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2011': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2012': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2013': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2014': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2015': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2016': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2017': 0})
        dis_df = dis_df.fillna({'house_landing_supply_acre_count_2018': 0})

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'购地-房地产大企业购地情况_index', index=True)
    return



def generate_index_fdcddkcrqk(corporate_start, corporate_end):

    """
    ***购地-房地产大地块出让情况***
    指标1：房地产公司出让总次数，总计1个，int
    指标2：房地产公司出让总面积，总计1个，int
    指标3：房地产公司不同土地用途供出让数量，总计8个，int
    指标4：房地产公司近5年出让总次数，总计1个，int
    指标5：房地产公司自2008年至2018年每年出让次数，总计11个，int
    指标6：房地产公司自2008年至2018年每年的出让面积，总计11个，int
    :return:
    """



    columns = ['house_landing_transfer_count',
               'house_landing_transfer_acre_count',
               'house_transfer_status_5',
               'house_transfer_status_6',
               'house_transfer_status_7',
               'house_transfer_status_8',
               'house_transfer_status_9',
               'house_transfer_status_10',
               'house_transfer_status_11',
               'house_transfer_status_12',
               'house_landing_transfer_in_last_5_years',
               'house_landing_transfer_count_2008',
               'house_landing_transfer_count_2009',
               'house_landing_transfer_count_2010',
               'house_landing_transfer_count_2011',
               'house_landing_transfer_count_2012',
               'house_landing_transfer_count_2013',
               'house_landing_transfer_count_2014',
               'house_landing_transfer_count_2015',
               'house_landing_transfer_count_2016',
               'house_landing_transfer_count_2017',
               'house_landing_transfer_count_2018',
               'house_landing_transfer_acre_count_2008',
               'house_landing_transfer_acre_count_2009',
               'house_landing_transfer_acre_count_2010',
               'house_landing_transfer_acre_count_2011',
               'house_landing_transfer_acre_count_2012',
               'house_landing_transfer_acre_count_2013',
               'house_landing_transfer_acre_count_2014',
               'house_landing_transfer_acre_count_2015',
               'house_landing_transfer_acre_count_2016',
               'house_landing_transfer_acre_count_2017',
               'house_landing_transfer_acre_count_2018']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'购地-房地产大地块出让情况')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]

        # 房地产公司出让总次数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 房地产公司出让总面积
        df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
        amount = df_temp.at['Row_sum', u'供地总面积'.encode('utf-8')]
        row_list.append(amount)
        total_num2 += amount

        # 房地产公司不同土地用途出让数量
        for status in range(1,9):
            y_df = df_temp.loc[df_temp[u'土地用途'.encode('utf-8')] == status]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)


        # 公司近5年出让总次数
        y_df = df_temp.loc[(df_temp['year0'] > 2013) & (df_temp['year0'] <=2019)]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)


        for year in range(2008,2019):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame['year0'] == year]


            # 房地产公司自2008年至2018年每年出让次数
            row_list.append(len(df_temp))
            total_num5 += len(df_temp)

            # 房地产公司自2008年至2018年每年的出让面积
            df_temp.loc['Row_sum'] = df_temp.apply(lambda x: x.sum())
            amount = df_temp.at['Row_sum', u'供地总面积'.encode('utf-8')]
            row_list.append(amount)
            total_num6 += amount

        row_dict[corporate] = row_list

        # 对空值进行处理以进行索引
        dis_df = dis_df.fillna({'house_landing_transfer_count_2008': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2009': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2010': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2011': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2012': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2013': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2014': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2015': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2016': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2017': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_count_2018': 0})

        dis_df = dis_df.fillna({'house_landing_transfer_acre_count': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2008': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2009': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2010': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2011': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2012': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2013': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2014': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2015': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2016': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2017': 0})
        dis_df = dis_df.fillna({'house_landing_transfer_acre_count_2018': 0})

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'购地-房地产大地块出让情况_index', index=True)
    return




def generate_index_jggg(corporate_start, corporate_end):

    """
    ***购地-结果公告***
    指标1：公司总购地数，总计1个，int
    指标2：公司购地总面积，总计1个，int
    指标3：公司不同土地用途购地数量，总计8个，int
    指标4：公司近5年购地次数，总计1个，int
    指标5：公司自2008年至2018年每年的购地数，总计11个，int
    指标6：公司自2008年至2018年每年的购地面积，总计11个，int
    :return:
    """



    columns = ['landing_purchasing_count',
               'status_5',
               'status_6',
               'status_7',
               'status_8',
               'status_9',
               'status_10',
               'status_11',
               'status_12',
               'landing_purchase_in_last_5_years',
               'landing_purchasing_count_2008',
               'landing_purchasing_count_2009',
               'landing_purchasing_count_2010',
               'landing_purchasing_count_2011',
               'landing_purchasing_count_2012',
               'landing_purchasing_count_2013',
               'landing_purchasing_count_2014',
               'landing_purchasing_count_2015',
               'landing_purchasing_count_2016',
               'landing_purchasing_count_2017',
               'landing_purchasing_count_2018']
    dis_df = pd.DataFrame(columns=columns)

    data_frame = fu.read_file_to_df(clean_data_temp_file_url, u'购地-结果公告')
    for corporate in range(corporate_start, corporate_end + 1):
        row_dict = {}
        row_list = []

        total_num1 = 0
        total_num2 = 0
        total_num3 = 0
        total_num4 = 0
        total_num5 = 0
        total_num6 = 0

        df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate]

        # 公司总购地数
        row_list.append(len(df_temp))
        total_num1 += len(df_temp)

        # 公司不同土地用途购地数量
        for status in range(1,9):
            y_df = df_temp.loc[df_temp[u'土地用途'.encode('utf-8')] == status]
            row_list.append(len(y_df))
            total_num3 += len(df_temp)


        # 公司近5年购地次数
        y_df = df_temp.loc[(df_temp['year0'] > 2013) & (df_temp['year0'] <=2019)]
        row_list.append(len(y_df))
        total_num4 += len(df_temp)


        for year in range(2008,2019):
            df_temp = data_frame[data_frame[u'企业编号'.encode('utf-8')] == corporate][
                data_frame['year0'] == year]


            # 公司自2008年至2018年每年的购地数
            row_list.append(len(df_temp))
            total_num5 += len(df_temp)

        row_dict[corporate] = row_list

        dis_df = dis_df.fillna({'landing_purchasing_count_2008': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2009': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2010': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2011': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2012': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2013': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2014': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2015': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2016': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2017': 0})
        dis_df = dis_df.fillna({'landing_purchasing_count_2018': 0})

        dis_df = dis_df.fillna({'landing_acre_count': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2008': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2009': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2010': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2011': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2012': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2013': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2014': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2015': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2016': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2017': 0})
        dis_df = dis_df.fillna({'landing_acre_count_2018': 0})

        dis_df = dis_df.append(pd.DataFrame(row_dict, index=columns).T, ignore_index=False)

    fu.write_file(dis_df, corporation_index_file_url, u'购地-结果公告_index', index=True)
    return



def append_score():
    """
    append score to each index file.
    :return:
    """
    score_frame = fu.read_file_to_df(working_file_url, u'企业评分')
    score_frame = score_frame.set_index(u'企业编号'.encode('utf-8'))

    for file_n in category_landing_purchase:
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
    for file_n in category_landing_purchase:
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
    for file_n in category_landing_purchase:
        print file_n

        data_frame = fu.read_file_to_df(corporation_index_file_url, file_n + '_index')
        data_frame['int_score'] = data_frame[u'企业总评分'.encode('utf-8')].apply(lambda x: round(x))

        fu.write_file(data_frame, corporation_index_file_url, file_n + '_index')


def pic_scatter():
    """
    plot scatter pictures for each index and score.
    :return:
    """
    vu.pic_scatter(category_landing_purchase, 'landing_purchase')

#
# indexes_filter = ['financing_count',
#                   'invest_year_between_2009_and_2013',
#                   'investment_amount_between_100million_and_500_million',
#                   'investment_amount_less_than_100_million',
#                   'investment_amount_more_than_500_million',
#                   'investment_year_after_2013',
#                   'investment_year_before_2009'
#                   ]


indexes_filter = []


def drop_useless_indexes_first_stage():
    edu.drop_useless_indexes(category_landing_purchase, indexes_filter)