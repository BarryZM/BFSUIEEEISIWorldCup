# *- coding:utf-8 -*-

"""
 module for soft assets data clean.
 including:
    专利
    产品
    作品著作权
    商标
    资质认证
    软著著作权
    项目信息
"""

import data_clean_utils as dcu
import file_utils
import primary_analysis as panaly
from file_directions import clean_data_temp_file_url
from files_category_info import category_soft_assets_files
import pandas


def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_soft_assets_files, u'软资产类')


def duplicate_handle():
    for name in category_soft_assets_files:
        dcu.merge_rows(name + '.xlsx')


def primary_analysis_after_duplicate_handled():
    """
    primary analysis after duplicate data handled
    :return:
    """
    panaly.list_category_columns_values(category_soft_assets_files, u'软资产类_dup_handled',
                                        file_url=clean_data_temp_file_url)
    return


# def work():
#     raw_files_primary_analysis()
#     duplicate_handle()
#     primary_analysis_after_duplicate_handled()

def empty_value_handle_patent():
    """

    :return:
    """
    dcu.drop_unit(u'专利', u'授权公告日'.encode('utf-8'), [u'同一申请的已公布的文献号', '-'], empty_mask='1000-01-01')
    dcu.drop_prefix_unit(u'专利', u'申请日'.encode('utf-8'), [u'公告日：'], empty_mask='1000-01-01')
    dcu.drop_unit(u'专利', u'申请日'.encode('utf-8'), ['-'], empty_mask='1000-01-01')

    panaly.list_category_columns_values([u'专利'], u'专利_empty_handled',
                                        file_url=clean_data_temp_file_url)
    return


def empty_value_handle_work():
    """

    :return:
    """
    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'作品著作权')
    values = {u'作品著作权类别'.encode('utf-8'): 9, u'作品著作权登记日期'.encode('utf-8'): '1000-01-01',
              u'作品著作权创作完成日期'.encode('utf-8'): '1000-01-01', u'作品著作权首次发布日期'.encode('utf-8'): '1000-01-01'}
    df = df.fillna(values)
    file_utils.write_file(df, clean_data_temp_file_url, u'作品著作权')

    status_1 = [u'A 文字', u'文字', u'文字作品']
    status_2 = [u'B 音乐', u'音乐', u'音乐作品']
    status_3 = [u'F 美术', u'美术', u'美术作品']
    status_4 = [u'G 摄影', u'摄影', u'摄影作品']
    status_5 = [u'H 电影', u'电影', u'电影作品和类似摄制电影的方法创造的作品', u'电影和类似摄制电影方法创作的作品', u'I 类似摄制电影方法创作作品', u'类似摄制电影方法创作的作品']
    status_6 = [u'J 工程设计图、产品设计图', u'工程设计图、产品设计图', u'工程设计图、产品设计图作品', u'建筑']
    status_7 = [u'K 地图、示意图', u'地图、示意图', u'图形']
    status_8 = [9]
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7, status_8]
    status_after = [1, 2, 3, 4, 5, 6, 7, 9]

    dcu.merge_status(u'作品著作权', u'作品著作权类别'.encode('utf-8'), status_list, status_after, others=8)

    # TODO Other columns
    return


def empty_value_handle_trademark():
    """
    Dirty value handle for table 商标.xlsx.
    First we'll drop rows that empty value is too many.
    # ['主营业务收入','净利润','利润总额','所有者权益合计', '纳税总额','营业总收入','负债总额','资产总额']
    # Once there are more than 3 empties in these 8 columns we will drop that row.
    Then we check nulls column by column and decide how to process with it.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    商标状态
    ------
    Empty percentage is 0.2597%(367 out of 141312). We replace them as 'Unknown'.

    -----------------------------
    申请日期
    ------
    Empty percentage is 0.3637%(514 out of 141312). We replace with '1000-01-01'.
    Others are well formatted.

    -----------------------------
    专用权期限开始日期
    ------
    All empty, drop it.

    -----------------------------
    专用权期限结束日期
    ------
    Empty percentage is 21.4922%(30371 out of 141312). This column's value can be extract from '商标使用期限时间段', so we
    drop it.
    -----------------------------
    商标使用期限时间段
    ------
    Empty percentage is 1.5915%(2249 out of 141312). We map them to '1000-01-01至1000-01-01'.
    Others are well formatted except some are '至', for these value we change to '1000-01-01至1000-01-01'.

    -----------------------------
    :return:
    """
    df = file_utils.read_file_to_df(clean_data_temp_file_url, u'商标')
    values = {u'商标状态'.encode('utf-8'): 'Unknown', u'申请日期'.encode('utf-8'): '1000-01-01',
              u'商标使用期限时间段'.encode('utf-8'): u'1000-01-01至1000-01-01'}
    df = df.fillna(values)
    file_utils.write_file(df, clean_data_temp_file_url, u'商标')

    dcu.drop_columns(u'商标', [u'专用权期限开始日期'.encode('utf-8')])
    dcu.drop_columns(u'商标', [u'专用权期限结束日期'.encode('utf-8')])

    status_1 = [u'至']
    status_list = [status_1]
    status_after = [u'1000-01-01至1000-01-01']

    dcu.merge_status(u'商标', u'商标使用期限时间段'.encode('utf-8'), status_list, status_after)
    return


def empty_value_handle_copyright():
    """
    Dirty value handle for table 软著著作权.xlsx.
    Next we should numeric all the value for future process.
    After these are done, it's time to work out features we can use in this table which belongs
        to exploratory data analysis.

    -----------------------------
    软件全称
    ------
    Nothing to do with it.

    -----------------------------
    软件著作权版本号
    ------
    Nothing to do with it.

    -----------------------------
    软件著作权登记批准日期
    ------
    Make time well formatted.

    -----------------------------
    :return:
    """
    dcu.time_unicode_format(u'软著著作权', u'软件著作权登记批准日期'.encode('utf-8'))


def primary_analysis_after_empty_handled():
    """
    primary analysis after empty data handled
    :return:
    """
    panaly.list_category_columns_values(category_soft_assets_files, u'软资产类_empty_handled',
                                        file_url=clean_data_temp_file_url)
    return


def numeric_patent():
    # numeric first
    status_1 = [u'发明专利', u'发明公布', u'发明公布更正', u'发明授权', u'发明授权更正']
    status_2 = [u'外观设计', u'外观设计更正']
    status_3 = [u'实用新型', u'实用新型更正']
    status_list = [status_1, status_2, status_3]
    status_after = [0, 1, 2]
    dcu.merge_status(u'专利', u'专利类型'.encode('utf-8'), status_list, status_after)
    return


def numeric_trademark():

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
    status_after = [0, 1, 2, 3, 4, 5, 6]
    dcu.merge_status(u'商标', u'商标状态'.encode('utf-8'), status_list, status_after, others=7)
    return


def numeric_certificate():
    # numeric first
    # 状态
    # valid
    status_1 = [u'有效',
                u'正常',
                u'当前批件',
                u'新立'
                ]
    # invalid
    status_2 = [u'已撤销',
                u'已暂停',
                u'已注销',
                u'已过期',
                u'注销',
                u'注销(非申请)',
                u'证书注销',
                u'过期失效',
                u'无效（依申请注销）',
                u'无效（逾期未换证）'
                ]
    status_list = [status_1, status_2]
    status_after = [0, 1]
    dcu.merge_status(u'资质认证', u'状态'.encode('utf-8'), status_list, status_after, others=2)

    # 证书名称
    # CCC
    status_1 = [u'CCC/null',
                u'CCC/低压电器',
                u'CCC/信息技术设备',
                u'CCC/儿童用品',
                u'CCC/农机产品',
                u'CCC/安全玻璃',
                u'CCC/安全防范产品',
                u'CCC/家用和类似用途设备',
                u'CCC/小功率电动机',
                u'CCC/无线局域网产品',
                u'CCC/机动车辆及安全附件',
                u'CCC/机动车辆轮胎',
                u'CCC/消防产品',
                u'CCC/照明电器',
                u'CCC/电信终端设备',
                u'CCC/电动工具',
                u'CCC/电焊机',
                u'CCC/电线电缆',
                u'CCC/电路开关及保护或连接用电器装置',
                u'CCC/装饰装修产品',
                u'CCC/音视频设备',
                u'CCC产品认证证书'
                ]
    status_2 = [u'质量管理体系认证（ISO9000）']

    status_3 = [u'高新技术企业认证']

    status_4 = [u'信息安全产品认证（未列入强制性产品认证目录内的信息安全产品）',
                u'信息安全服务资质认证',
                u'信息安全管理体系认证',
                u'信息技术服务管理体系认证',
                u'计算机信息系统集成项目经理资质证书',
                u'计算机信息系统集成高级项目经理资质证书',
                ]
    status_5 = [u'医疗器械注册证',
                u'医疗器械生产企业许可证',
                u'医疗器械经营企业许可证',
                u'医疗器械质量管理体系认证'
                ]

    status_6 = [u'建筑 - 勘察资质',
                u'建筑 - 建筑业企业资质',
                u'建筑 - 招标代理资格',
                u'建筑 - 监理资质',
                u'建筑 - 设计与施工一体化资质',
                u'建筑 - 设计资质',
                u'建筑业企业资质',
                u'建筑业资质证书',
                u'建筑施工资质证书',
                u'建设施工行业质量管理体系认证'
                ]

    status_7 = [u'环保产品认证',
                u'环境标志产品',
                u'环境管理体系认证',
                ]
    status_list = [status_1, status_2, status_3, status_4, status_5, status_6, status_7]
    status_after = [0, 1, 2, 3, 4, 5, 6]
    dcu.merge_status_new_column(u'资质认证', u'证书名称'.encode('utf-8'), 'categories', status_list, status_after, others=7)
    return


def numeric_program():
    # data_frame = file_utils.read_file_to_df(clean_data_temp_file_url, u'项目信息')
    # data_frame['industry'] = data_frame[u'标签'.encode('utf-8')].apply(
    #     lambda x: dcu.cal_industry(x))
    # file_utils.write_file(data_frame, clean_data_temp_file_url, u'项目信息', index=True)

    panaly.list_category_columns_values([u'项目信息'], u'项目信息_empty_handled',
                                        file_url=clean_data_temp_file_url)


def work_():
    duplicate_handle()
    print('duplicate_handle() done!')
    empty_value_handle_patent()
    print('empty_value_handle_patent() done!')
    empty_value_handle_work()
    print('empty_value_handle_work() done!')
    empty_value_handle_trademark()
    print('empty_value_handle_trademark() done!')
    empty_value_handle_copyright()
    print('empty_value_handle_copyright() done!')
    numeric_patent()
    print('numeric_patent() done!')
    numeric_trademark()
    print('numeric_trademark() done!')
    numeric_certificate()
    print('numeric_certificate() done!')
    return
