# *- coding:utf-8 -*-

import file_utils as fu
from file_directions import corporation_index_file_url, corporation_index_scatter_file_url
import numpy as np
# Visualization
import matplotlib.pyplot as plt

# matplotlib inline
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 16
plt.rcParams['patch.edgecolor'] = 'k'


def pic_scatter(index_files, category_name, index_file_url=corporation_index_file_url,
                scatter_url=corporation_index_scatter_file_url):
    for file_n in index_files:
        print file_n
        data_frame = fu.read_file_to_df(index_file_url, file_n + '_index')
        for column in data_frame.columns:
            if column == 'Unnamed: 0':
                continue
            plt.figure(figsize=(14, 9))

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

            plt.savefig(fu.check_file_url(
                scatter_url + '/' + category_name + '/' + file_n + '/') + column + '.png', dpi=150)
            plt.close()
