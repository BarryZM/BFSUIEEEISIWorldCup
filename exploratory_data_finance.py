# *- coding:utf-8 -*-

"""
 Exploratory data utils
"""
import sys
import pandas
import numpy


reload(sys)
sys.setdefaultencoding('utf-8')

# 计算季度增长率
def seasonal_growth_rate(file_name, column_names, new_file, empty_mask='Unknown', file_url=clean_data_temp_file_url,
                    dst_file_url=clean_data_temp_file_url):
    """
    :param file_name: 来源表的名字
    :param column_names: 需要计算增长率的列名向量
    :param new_file: 输出表的名字
    :param empty_mask: 空值的标志
    :param file_url: 输入来源
    :param dst_file_url: 输出来源，需要改成新文件夹
    :return:
    """
    data_frame = file_utils.read_file_to_df(file_url, file_name)

    for index in range(0, len(data_frame)):_
        j = 0
        c_name[j]=


    for i in range(0, 6): _
        c_name[j] = i*10
        j=j+1


data_frame.set_value(i - 1000, 0, i)

    a = pd.DataFrame(index = [range(1001,3001)],columns = ['a', 'b', 'c'])
    new_data_frame
     #新矩阵
    new_data_frame.set_value(0, 0, u'公司编号')




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


            if 下一行，编号=本行编号 & 下一行，时间 < 本行，时间
            上季度数字 = 下一行，本列
        else 上季度数字=空
        end
        if 季度数字=float & 上季度数字=float
        （公司_季度，指标_增长率）=（季度数字 - 上季度数字）*100 /（上季度数字 * 月份差 / 3）
        else （公司_季度，指标_增长率）= unknown
        end
        end
        end
写new_data
file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), new_file,
                      sheet_name='Sheet', index=False)

# try

    for i in range(1,5):
        for j in range(1,5):
            i_j=i+j
    print 2_3