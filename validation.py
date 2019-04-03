# *- coding:utf-8 -*-

"""
 module for validation by RMSE
"""
from math import sqrt


def cal_rmse(prediction, target):
    error = []
    for i in range(len(target)):
        error.append(target[i] - prediction[i])

    squared_error = []
    abs_error = []
    for val in error:
        squared_error.append(val * val)  # target-prediction之差平方
        abs_error.append(abs(val))  # 误差绝对值

    print("RMSE = " + str(sqrt(sum(squared_error) / len(squared_error))))  # 均方根误差RMSE
    print("MAE = " + str(sum(abs_error) / len(abs_error)))  # 平均绝对误差MAE