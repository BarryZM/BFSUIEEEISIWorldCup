# *- coding:utf-8 -*-

import file_utils as fu
from file_directions import corporation_index_file_url, corporation_index_scatter_file_url, \
    corporation_index_heat_map_file_url
import numpy as np
import seaborn as sns

# Visualization
import matplotlib.pyplot as plt

# matplotlib inline
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 14
plt.rcParams['patch.edgecolor'] = 'k'
plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False


def pic_scatter(index_files, category_name, index_file_url=corporation_index_file_url,
                scatter_url=corporation_index_scatter_file_url):
    """
    scatter picture for each index and the score.
    :param index_files: the index file we need to analyse.
    :param category_name: the category of the index, the images will be stored at this file folder.
    :param index_file_url: file url to index files.
    :param scatter_url: scatter image url to be stored.
    :return:
    """
    fig = plt.figure(figsize=(14, 9))
    for file_n in index_files:
        print file_n
        data_frame = fu.read_file_to_df(index_file_url, file_n + '_index')
        for column in data_frame.columns:
            if column == 'Unnamed: 0':
                continue

            plt.title(column)
            plt.xlabel('score')
            plt.ylabel(column)

            x = data_frame['int_score'].to_list()
            y = data_frame[column].to_list()
            xy = list(zip(x, y))

            s = []
            c = np.random.rand(len(xy))
            for xy_item in xy:
                s.append(xy.count(xy_item) * 1.5)
            plt.scatter(x, y, s=s, c=c)

            # plt.show()

            fig.savefig(fu.check_file_url(
                scatter_url + '/' + category_name + '/' + file_n + '/') + str(column).replace('/', '-') + '.png',
                        dpi=150)
            plt.clf()


def pic_corr_heat_map(index_files, category_name, index_file_url=corporation_index_file_url,
                      heat_map_url=corporation_index_heat_map_file_url):
    fig = plt.figure(figsize=(26, 18))
    for file_n in index_files:
        print file_n
        data_frame = fu.read_file_to_df(index_file_url, file_n + '_index')
        data_frame = data_frame.drop(columns=['Unnamed: 0', u'企业总评分'.encode('utf-8')])
        corr_matrix = data_frame.corr()
        print (corr_matrix)
        sns.heatmap(corr_matrix, annot=True, vmax=1, vmin=0, xticklabels=True, yticklabels=True, square=True)
        plt.title(file_n)

        fig.savefig(fu.check_file_url(
            heat_map_url + '/' + category_name + '/') + file_n + '.png', dpi=75)
        plt.clf()
