# *- coding:utf-8 -*-

"""
 Exploratory data utils
"""
import sys
import pandas
import numpy
import file_utils
from file_directions import working_file_url, clean_data_temp_file_url
import pandas


#把面板数据变成截面数据，先建立空表
#def cross_section(file_name, vars, empty_mask='Unknown', file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):
    """

    :param file_name:
    :param vars: 需要和时间交叉的变量集，写成向量
    :param empty_mask:
    :param file_url:
    :param dst_file_url:
    :return:
    """
    # try
    file_name=u'上市公司财务信息-每股指标'
    vars=[u'基本每股收益(元)', u'扣非每股收益(元)',u'稀释每股收益(元)',
        u'每股净资产(元)',u'每股公积金(元)',u'每股未分配利润(元)',u'每股经营现金流(元)']
    file_url = clean_data_temp_file_url
    dst_file_url = clean_data_temp_file_url

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    date = data_frame[u'日期']  # 日期列
    unique_date = list(set(date)) #删除重复

    #新表的列名，是变量名和日期的交叉项
    var_date=[]
    for i in range(0,len(vars)):
        for j in range(0,len(unique_date)):
            var_date.append(vars[i]+ unique_date[j].encode('utf-8'))
"""
    尝试
    a = []
    aa=[1,2,3]
    a = pandas.DataFrame(index=[range(1001, 3001)], columns=aa)
#   输出时文件名需要加上''，index=true表示包含第一列
    file_utils.write_file(a, file_utils.check_file_url(dst_file_url), 'a',ext='.xlsx',
                          sheet_name='Sheet', index='true')    
    
"""

# 建立空表并保存
    b = []
    b = pandas.DataFrame(index = [range(1001,3001)],columns = var_date)
file_utils.write_file(b, file_utils.check_file_url(dst_file_url), 'b', ext='.xlsx',
                      sheet_name='Sheet', index='true')


new_data_frame=[]
     #新矩阵
    new_data_frame.set_value(0, 0, u'公司编号')



aa=u'以'
bb=u'以也'
cc=aa+bb

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for column_names in range(0,len(column_names)):
        for index in range(0, len(data_frame)):
            this_season = data_frame.at[index, u'日期']
            this_number = data_frame.at[index, column_name]
            company = data_frame.at[index, 0]
            if data_frame.at[index+1, 0]==data_frame.at[index, 0] and  data_frame.at[index+1, u'日期']<data_frame.at[index, u'日期']: #时间比较
                last_season = data_frame.at[index+1, u'日期']
                last_number = data_frame.at[index+1, column_name]
            elif:
                last_number = 'Unknown'
            if isinstance(this_number,float)==1 and isinstance(last_number,float)==1:

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return