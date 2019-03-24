# *- coding:utf-8 -*-

"""
 module for landing purchase data clean.
 including:


 Empty values are mostly replaced by -1.
"""

import data_clean_utils as dcu
import file_utils as fu
import primary_analysis as panaly
from file_directions import clean_data_temp_file_url
from files_category_info import category_landing_purchase




def raw_files_primary_analysis():
    """
    primary analysis for raw files without handled
    :return:
    """
    panaly.list_category_columns_values(category_landing_purchase, u'地产类')
    return


#  TODO handle all the duplicate data in all tables listed in '地产类'



def duplicate_handle():
    for name in category_landing_purchase:
        dcu.merge_rows(name + '.xlsx')
        return



def primary_analysis_after_duplicate_handled():

    panaly.list_category_columns_values(category_landing_purchase, u'地产类_dup_handled',
                                        file_url=clean_data_temp_file_url)
    return

