# *- coding:utf-8 -*-

"""
 module for competing products data clean.
 including:


 Empty values are mostly replaced by -1.
"""

import data_clean_utils as dcu
import primary_analysis as panaly
from files_category_info import category_paying_taxes
from file_directions import clean_data_temp_file_url
import file_utils as fu


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_paying_taxes, u'纳税类')


# TODO handle all the duplicate data in all tables listed in '纳税类'


def duplicate_handle():
    for name in category_paying_taxes:
        dcu.merge_rows(name + '.xlsx')


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_paying_taxes, u'纳税类_dup_handled',
                                        file_url=clean_data_temp_file_url)


# def empty_value_handle_basic_info():
#     """
#     empty_value handle for table 年报-企业基本信息.
#     :return:
#     """
#     empty_check_list = [u'纳税人资格',
#                         u'有效截止日期',
#                         u'纳税人状态',
#                         u'是否具有一般纳税人资格',
#                         u'登记注册类型',
#                         u'出口状态备案状态']
#     dcu.drop_rows_too_many_empty(u'一般纳税人.xlsx', columns=empty_check_list, thresh=4)
#     # panaly.list_category_columns_values([u'一般纳税人'], u'一般纳税人_empty_handled',
#     #                                     file_url=clean_data_temp_file_url)
#     return

def pre_clean():
    file_name = u'一般纳税人'
    dcu.merge_status(file_name, u'认定日期'.encode('utf-8'), [], [], empty_mask='0000-00-00')
    dcu.merge_status(file_name, u'纳税人状态'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'出口状态备案状态'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'登记注册类型'.encode('utf-8'), [], [], empty_mask='Unknown')
    dcu.merge_status(file_name, u'纳税人资格'.encode('utf-8'), [], [], empty_mask='Unknown')

    dcu.drop_columns(file_name, u'有效日期期起'.encode('utf-8'))
    dcu.drop_columns(file_name, u'有效截止日期'.encode('utf-8'))
    dcu.drop_columns(file_name, u'是否具有一般纳税人资格'.encode('utf-8'))
    dcu.drop_columns(file_name, u'扣缴义务'.encode('utf-8'))
    dcu.drop_columns(file_name, u'是否按季申报'.encode('utf-8'))

    return





def rearrange_excel():
    """

    :return:
    """
    wr1 = fu.read_file_to_df(clean_data_temp_file_url, u'一般纳税人.xlsx',
                             sheet_name='Sheet')
    wr1.ix[wr1[u'纳税人资格'.encode('utf-8')].str.contains(u'出口退（免）税企业'), [u'出口状态备案状态'.encode('utf-8')]] = u'出口退（免）税企业'
    fu.write_file(wr1, clean_data_temp_file_url, u'一般纳税人', ext='.xlsx',
                  sheet_name='Sheet', index=False)


"""
    Dirty value handle for table 纳税A级年份.xlsx.
    We check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
    to exploratory data analysis. 

    -----------------------------
    纳税A级年份
    ------
    Empty percentage is 100%(6885 out of 6885).
    4 status can be concluded in this part, they are [‘2014’，‘2015’，‘2016’，‘2017’]
    and there are no another status for the empty value.
    So we can map these total 4 status to three: {‘2014’:0,‘2015’:1,'2016’:2,‘2017’:3,'Unknown':-6}.
    -----------------------------
"""

"""
    Dirty value handle for table 一般纳税人.xlsx.
    First we'll drop rows that empty value is too many.
    # ['纳税人资格','有效截止日期','纳税人状态','是否具有一般纳税人资格','登记注册类型','出口状态备案状态']
    # Once there are more than 4 empties in these 6 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
    to exploratory data analysis. 

    -----------------------------
    纳税人资格
    ------
    Empty percentage is 11.63%(316 out of 2716).
    23 status this value has, they are ['一般纳税人','其他','内资企业采购国产设备','出口退（免）税企业','增值税一般纳税人'
    '增值税小规模纳税人','增值税汇总纳税企业','外商投资企业','外资企业采购国产设备','按征收率征收增值税小规模纳税人',
    '按适用税率征收增值税小规模纳税人','有进出口经营权的外贸公司','消费税汇总纳税企业','简易办法征收一般纳税人',
    '经济实体（安置富余人员）','资源综合利用企业','软件及集成电路生产企业', '辅导期增值税一般纳税人','金银首饰消费税纳税人',
    '销售供出口货物企业','非一般纳税人','饲料产品企业','高新技术产业企业'].
    We just add another status for the empty value:'Unknown'.
    -----------------------------
    认定日期
    ------
    Empty percentage is 49.63%(1348 out of 2716).
    We consider each part as an independent status, for these empty value, we just add another status: 'Unknown'
    As there are so many empty values and the information for this column isn't very important.
    So we decide to drop this column.
    -----------------------------
    有效日期期起
    ------
    Empty percentage is 58.06%(1577 out of 2716).
    We consider each part as an independent status, for these empty value, we just add another status: 'Unknown'
    As there are so many empty values and the information for this column isn't very important.
    So we decide to drop this column.
    -----------------------------
    有效截止日期
    ------
    Empty percentage is 57.36%(1558 out of 2716).
    We consider each part as an independent status, for these empty value, we just add another status: 'Unknown'
    According to the deadline of taxes, we set up a time (2019-01-01) as the deadline to divide the values. The values
    before 2019-01-01, we could judge that the column of "纳税人状态" is abnormal if that column is empty. The values
    after 2019-01-01, we could judge that the column of "纳税人状态" is normal if that column is empty. the unknown part
    will be a specific type in these values.
    -----------------------------
    是否具有一般纳税人资格
    ------
    Empty percentage is 92.16%(2503 out of 2716).
    2 status this value has, they are ['是','否'].
    We just add another status for the empty value:'Unknown'.
    So we can map these total 3 status to three: {‘是’:0,‘否’:1,'Unknown':-1}.
    -----------------------------
    纳税人状态
    ------
    Empty percentage is 68.41%(1854 out of 2716).
    2 status this value has, they are ['是','注销报验','正常','注销'].
    We just add another status for the empty value:'Unknown'.
    We can simply believe that the status of '是' and '正常' is similar and the status of '注销报验' and '注销' is similar.
    And based on the counts for every status, we simplify these status to ['正常','注销','Unknown']
    So we can map these total 3 status to three: {'正常':0,‘注销’:1,'Unknown':-1}.
    -----------------------------
    登记注册类型
    ------
    Empty percentage is 76.91%(2089 out of 2716).
    2 status this value has, they are ['是','注销报验','正常','注销'].
    19 status this value has, they are ['中外合资经营企业','其他','其他企业','其他有限责任公司','合资经营企业（港或澳、台资）'
    '国有企业','国有相对控股上市企业','国有相对控股非上市企业','国有绝对控股上市企业','国有绝对控股非上市企业','外商投资股份有限公司',
    '外资企业','港、澳、台商投资股份有限公司','私营有限责任公司','私营股份有限公司','股份合作企业','集体企业','非国有控股上市企业',
    '非国有控股非上市企业'].
    We just add another status for the empty value:'Unknown'.
    We can simply believe that the status of '其他','其他企业','其他有限责任公司','非国有控股上市企业','非国有控股非上市企业'
    can be combined to '其他企业'. And '中外合资经营企业', '合资经营企业（港或澳、台资）' can be combined to '合资企业'.
    '国有企业','国有相对控股上市企业','国有相对控股非上市企业', '国有绝对控股上市企业','国有绝对控股非上市企业' can be combined
    to '国有企业'. '外商投资股份有限公司', '外资企业','港、澳、台商投资股份有限公司' can be combined to '外资企业',
    '私营有限责任公司','私营股份有限公司' can be combined to‘私营企业’, '股份合作企业','集体企业' can be combined to '集体企业'.
    So we can map these total 7 status to three: {'其他企业':0,‘合资企业’:1,'国有企业':2,'外资企业':3,'私营企业':4,
    '集体企业':5,'Unknown':-1}
    -----------------------------
    扣缴义务
    ------
    Empty percentage is 89.99%(2444 out of 2716).
    1 status this value has, it is ['依法确定'].
    We just add another status for the empty value:'Unknown'.
    As there are so many empty values and the information for this column isn't very important.
    So we decide to drop this column.
    -----------------------------
    出口状态备案状态
    ------
    Empty percentage is 86.92%(2361 out of 2716).
    2 status this value has, they are ['出口退（免）税企业','非出口退（免）税企业'].
    Considering that the column "纳税人资格" also have the value about "出口退（免）税企业", so we could add some values
    with  the status '出口退（免）税企业'
    We just add another status for the empty value:'Unknown'.
    So we can map these total 3 status to three: {'出口退（免）税企业':0,‘非出口退（免）税企业’:1,'Unknown':-1}.
    -----------------------------
    是否按季申报
    ------
    Empty percentage is 88.33%(2399 out of 2716).
    3 status this value has, they are ['yes','季','月'].
    We just add another status for the empty value:'Unknown'.
    As there are so many empty values and the information for this column isn't very important.
    So we decide to drop this column.
    -----------------------------


"""
def time_split(file_name, column_name, i = 0):
    df = fu.read_file_to_df(clean_data_temp_file_url, file_name, sheet_name='Sheet')  # 读取工作表
    df["year"+str(i)], df["month"+str(i)], df["day"+str(i)] = df[column_name].str.split("-", n=2).str  # 分成三个表 n为劈开的次数
    df.drop(column_name, axis=1, inplace=True)  # 删除原有的列
    fu.write_file(df, clean_data_temp_file_url, file_name, ext='.xlsx', sheet_name='Sheet', index=False) # 保存
    return




def kind_taxers(file_name, column_name):
    status_1 = [u'增值税一般纳税人', u'增值税汇总纳税企业', u'外商投资企业', u'外资企业采购国产设备', u'简易办法征收一般纳税人',
                u'辅导期增值税一般纳税人',u'一般纳税人']
    status_2 = [u'出口退（免）税企业', u'内资企业采购国产设备', u'有进出口经营权的外贸公司', u'经济实体（安置富余人员）',
                u'资源综合利用企业', u'软件及集成电路生产企业', u'销售供出口货物企业', u'饲料产品企业', u'高新技术产业企业']
    status_3 = [u'增值税小规模纳税人', u'按征收率征收增值税小规模纳税人', u'按适用税率征收增值税小规模纳税人', u'非一般纳税人']
    status_4 = [u'其他', u'消费税汇总纳税企业', u'金银首饰消费税纳税人']
    status_no = ['Unknown']
    status_list = [status_1, status_2, status_3, status_4, status_no]
    status_after = [1, 2, 3, 4, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def status_taxers(file_name, column_name):
    status_1 = [u'是',u'正常']
    status_2 = [u'报验']
    status_3 = [u'核销报验',u'注销']
    status_no = ['Unknown']
    status_list = [status_1, status_2, status_3, status_no]
    status_after = [1, 2, 3, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def status_register(file_name, column_name):
    status_1 = [u'国有企业',u'国有相对控股上市企业', u'国有相对控股非上市企业', u'国有绝对控股上市企业', u'国有绝对控股非上市企业']
    status_2 = [ u'股份合作企业', u'集体企业']
    status_3 = [u'私营有限责任公司',u'私营股份有限公司']
    status_4 = [u'外商投资股份有限公司', u'外资企业', u'港、澳、台商投资股份有限公司']
    status_5 = [u'中外合资经营企业', u'合资经营企业（港或澳、台资）']
    status_6 = [ u'其他',u'其他企业',u'其他有限责任公司',u'非国有控股上市企业',u'非国有控股非上市企业']
    status_no = ['Unknown']
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_no]
    status_after = [1, 2, 3, 4, 5, 6, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def status_export(file_name, column_name):
    status_1 = [u'出口退（免）税企业']
    status_2 = [u'非出口退（免）税企业']
    status_no = ['Unknown']
    status_list = [status_1, status_2, status_no]
    status_after = [1, 2, -1]
    dcu.merge_status(file_name, column_name, status_list, status_after)
    return


def clean_tax():
    file_name = u'一般纳税人'
    # dcu.merge_status(file_name, u'认定日期'.encode('utf-8'), [], [], empty_mask='Unknown')
    # dcu.merge_status(file_name, u'纳税人状态'.encode('utf-8'), [], [], empty_mask='Unknown')
    # dcu.merge_status(file_name, u'出口状态备案状态'.encode('utf-8'), [], [], empty_mask='Unknown')
    #
    #
    # dcu.drop_columns(file_name, u'有效日期期起'.encode('utf-8'))
    # dcu.drop_columns(file_name,u'有效截止日期'.encode('utf-8'))
    # dcu.drop_columns(file_name, u'是否具有一般纳税人资格'.encode('utf-8'))
    # dcu.drop_columns(file_name, u'扣缴义务'.encode('utf-8'))
    # dcu.drop_columns(file_name, u'是否按季申报'.encode('utf-8'))


    kind_taxers(file_name, u'纳税人资格'.encode('utf-8'))
    status_taxers(file_name, u'纳税人状态'.encode('utf-8'))
    status_export(file_name, u'出口状态备案状态'.encode('utf-8'))
    status_register(file_name, u'登记注册类型'.encode('utf-8'))

    dcu.time_unicode_format(file_name, column_name=u'认定日期'.encode('utf-8'))
    time_split(file_name, u'认定日期'.encode('utf-8'), i = 0)

    return
