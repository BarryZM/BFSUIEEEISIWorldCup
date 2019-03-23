# *- coding:utf-8 -*-

"""
 Data clean utils
"""
import sys

import file_utils
from file_directions import working_file_url, clean_data_temp_file_url
import pandas

reload(sys)
sys.setdefaultencoding('utf-8')


def merge_rows(file_name, keys=None, file_url=working_file_url, dst_file_url=clean_data_temp_file_url):
    """
    merge a table's rows with the same unique keys.
    :param file_name:
    :param keys:
    :param file_url:
    :param dst_file_url: which file folder should store the result
    :return:
    """
    # origin_df = file_utils.read_file(working_file_url + file_name)
    # data_frame = origin_df
    # data_frames = [data_frame]
    #
    # str_keys = []
    # for index in range(1, len(origin_df)):
    #     anchor_row = origin_df[index - 1:index]
    #
    #     temp_df = origin_df[index:]
    #     for key in keys:
    #         if index == 1:
    #             str_keys.append(key.encode('utf-8'))
    #         temp_df = temp_df.loc[temp_df[key.encode('utf-8')] == anchor_row.loc[index-1, key.encode('utf-8')]]
    #
    #     duplicated_num = len(temp_df)
    #     for j in range(0, duplicated_num):
    #         data_frames[0] = data_frames[0].drop(index=index)
    #
    #     for frame_nums in range(1, duplicated_num + 1):
    #         if len(data_frames) > frame_nums:
    #             data_frames[frame_nums] = data_frames[frame_nums].append(temp_df[frame_nums - 1: frame_nums])
    #         else:
    #             new_df = temp_df[frame_nums - 1: frame_nums]
    #             data_frames.append(new_df)
    #
    #     index += duplicated_num
    #
    # data_frame = data_frames[0]
    # for df in data_frames:
    #     data_frame = pandas.merge(data_frame, df, how='left', on=origin_df.columns.tolist())

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    data_frame = data_frame.drop_duplicates()

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)

    return


def drop_rows_too_many_empty(file_name, columns, thresh=2, file_url=clean_data_temp_file_url,
                             dst_file_url=clean_data_temp_file_url):
    """
    drop rows that too many values are empty.
    :param file_name:
    :param columns: the columns we need to check if it is empty
    :param thresh: how many empty is 'too many'
    :param file_url: input file url
    :param dst_file_url: where to store the result
    :return:
    """
    data_frame = file_utils.read_file_to_df(file_url, file_name)
    data_frame = data_frame.dropna(subset=columns, thresh=thresh)

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return


def drop_columns(file_name, columns, file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    data_frame = data_frame.drop(columns, axis=1)

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return


def merge_status(file_name, column_name, status, status_names, empty_mask='Unknown', file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):
    """

    :type status_names: list
    :type status: list
    """
    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if pandas.isnull(content) or pandas.isna(content):
            data_frame.set_value(index, column_name, empty_mask)
        for j in range(0, len(status)):
            if content in status[j]:
                data_frame.set_value(index, column_name, status_names[j])

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return

# 把万，亿，万亿结尾的金额改为数字
def change_number(file_name, column_name, file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):
    """

    :type status_names: list
    :type status: list
    """
    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if str(content).endswith(u'万'):
            num=str(content).replace(u'万', '') # 把前面的改成后面的，此处是删去结尾的'万'
            numb=float(num)
            data_frame.set_value(index, column_name, numb*(10**4))
        elif str(content).endswith(u'万亿'):
            num=str(content).replace(u'万亿', '') # 把前面的改成后面的，此处是删去结尾的'万'
            numb=float(num)
            data_frame.set_value(index, column_name, numb*(10**12))
        elif str(content).endswith(u'亿'):
            num = str(content).replace(u'亿', '')  # 把前面的改成后面的，此处是删去结尾的'万'
            numb = float(num)
            data_frame.set_value(index, column_name, numb * (10 ** 8))

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return


def mark_invalid_num_data(file_name, column_name, operator, thresh_value, error_mask=-1, file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if not (isinstance(content, float) or isinstance(content, int)):
            continue

        isvalid = True
        if operator == '<':
            isvalid = not (content < thresh_value)
        elif operator == '>':
            isvalid = not (content > thresh_value)
        elif operator == '>=':
            isvalid = not (content >= thresh_value)
        elif operator == '<=':
            isvalid = not (content <= thresh_value)

        if not isvalid:
            data_frame.set_value(index, column_name, error_mask)

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return


def drop_invalid_data(file_name, column_name, operator, thresh_value, file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if not (isinstance(content, float) or isinstance(content, int)):
            continue

        isvalid = True
        if operator == '<':
            isvalid = not (content < thresh_value)
        elif operator == '>':
            isvalid = not (content > thresh_value)
        elif operator == '>=':
            isvalid = not (content >= thresh_value)
        elif operator == '<=':
            isvalid = not (content <= thresh_value)

        if not isvalid:
            data_frame = data_frame.drop(index=index)

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return


def drop_unit(file_name, column_name, unit_strs, empty_mask='Unknown', file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):
    """

    :type unit_strs: list
    """
    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if pandas.isnull(content) or pandas.isna(content):
            data_frame.set_value(index, column_name, empty_mask)
        for j in range(0, len(unit_strs)):
            if str(content).endswith(unit_strs[j]):
                data_frame.set_value(index, column_name, str(content).replace(unit_strs[j], ''))

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return


def extract_keyword(file_name, column_name, keywords, empty_mask='Unknown', others_mask='Others', file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):

    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if pandas.isnull(content) or pandas.isna(content):
            data_frame.set_value(index, column_name, empty_mask)
        for j in range(0, len(keywords)):
            if keywords[j] in str(content):
                data_frame.set_value(index, column_name, keywords[j])

    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if content not in keywords:
            data_frame.set_value(index, column_name, others_mask)

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)
    return


def time_periods_format(file_name, column_name, file_url=clean_data_temp_file_url, dst_file_url=clean_data_temp_file_url):
    data_frame = file_utils.read_file_to_df(file_url, file_name)
    for index in range(0, len(data_frame)):
        content = data_frame.at[index, column_name]
        if pandas.isnull(content) or pandas.isna(content):
            data_frame.set_value(index, column_name, '-')
            continue
        if u'年' in content:
            content = str(content).replace('-', '~').replace(u'年', '/').replace(u'月', '/').replace(u'日', '')
        elif '~' in content:
            content = str(content).replace('-', '/')
        elif u'至' in content:
            content = str(content).replace(u'至', '~').replace('-', '/')
        content = str(content).replace('/0', '/')

        data_frame.set_value(index, column_name, content)

    file_utils.write_file(data_frame, file_utils.check_file_url(dst_file_url), file_name,
                          sheet_name='Sheet', index=False)