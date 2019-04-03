# *- coding:utf-8 -*-

origin_file_url = u'data/赛题1数据材料/赛题1数据集/赛题1数据集/'  # the original file folder url, files in it should be read only
working_file_url = u'data/processed_data/raw_data/'  # the working file folder, a copy from the original file folder, can be changed during work
statistic_data_file_url = u'data/processed_data/statistic_data/'  # statistic info for every table
categorized_data_file_url = u'data/processed_data/categorized_data/'  # categorized info for every table
cleaned_data_file_url = u'data/processed_data/cleaned_data/'  # cleaned tables
clean_data_temp_file_url = u'data/processed_data/clean_data_temp/'  # clean temp tables
corporation_index_file_url = u'data/processed_data/corporation_index/'  # corporation index files
corporation_index_scatter_file_url = u'data/processed_data/corporation_index_scatter/'  # corporation index scatter image files
corporation_index_heat_map_file_url = u'data/processed_data/corporation_index_heat_map/'  # corporation index heatmap image files

corporate_index_false = u'企业总评分'.encode('utf-8')
corporate_index_true = u'企业编号'.encode('utf-8')