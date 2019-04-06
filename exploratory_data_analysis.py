# *- coding:utf-8 -*-

"""
 module for EDA(exploratory data analysis)
"""
import os
import file_utils as fu
from file_directions import corporation_index_file_url, corporation_index_second_stage_file_url


def score_integerize(file_holder_url):
    """
    scores are float, and we want try if integers will helps.
    :return:
    """
    for file_n in os.listdir(file_holder_url):
        if file_n.startswith('.') or file_n.startswith('second_stage'):  # ignore .DS_Store and file folder
            continue
        print file_n

        data_frame = fu.read_file_to_df(file_holder_url, file_n)
        data_frame['int_score_root'] = data_frame[u'企业总评分'.encode('utf-8')].apply(lambda x: int(x))

        fu.write_file(data_frame, file_holder_url, file_n)


def work():
    score_integerize(corporation_index_file_url)
    score_integerize(corporation_index_second_stage_file_url)
    return
