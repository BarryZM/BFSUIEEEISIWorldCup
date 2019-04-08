# *- coding:utf-8 -*-

"""
 module for models
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, make_scorer
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBClassifier
import validation
import pandas as pd
import numpy as np

# Custom scorer for cross validation
scorer = make_scorer(f1_score, greater_is_better=True, average='macro')


def get_fitted_data_set(train_set, test_set):
    features = list(train_set.columns)
    pipeline = Pipeline([('imputer', Imputer(strategy='median')),
                         ('scaler', MinMaxScaler())])

    # Fit and transform training data
    train_set = pipeline.fit_transform(train_set)
    test_set = pipeline.transform(test_set)
    return train_set, test_set, features


def random_forest(data, target, test_data, test_target, features=None):
    # for n in range(407, 410):
        n = 408  # 408 seems best with max_features 59 in these values
        print ('n = ' + str(n))
        model = RandomForestClassifier(n_estimators=n, random_state=10, n_jobs=-1, max_features=59)
        model.fit(data, target)
        prediction_fit = model.predict(data)
        prediction = model.predict(test_data)
        cv_score = cross_val_score(model, data, target, cv=10, scoring=scorer)
        # print(prediction)
        # print(test_target)
        print ('F1 score = ' + str(cv_score.mean()))
        print ('F1 score std = ' + str(cv_score.std()))
        # Feature importances into a dataframe
        # if features is not None:
        #     feature_importances = pd.DataFrame({'feature': features, 'importance': model.feature_importances_})
        #     # print(feature_importances.head())
        validation.cal_rmse(prediction, test_target)
        return prediction_fit, prediction


def random_forest_kneighbours_reg(data, target, reg_target, test_data, test_target, features=None):
    prediction_fit, prediction = random_forest(data, target, test_data, test_target, features)
    data = np.c_[data, prediction_fit]
    test_data = np.c_[test_data, prediction]
    kneighbors_reg(data, reg_target, test_data, test_target)


def divide_num(x):
    n = 3
    return int(x/n) * n


def random_forest_linear_reg(data, target, reg_target, test_data, test_target, features=None):
    prediction_fit, prediction = random_forest(data, map(divide_num, target), test_data, test_target, features)
    data = np.c_[data, prediction_fit]
    test_data = np.c_[test_data, prediction]
    prediction_fit, prediction = random_forest(data, target, test_data, test_target, features)
    data = np.c_[data, prediction_fit]
    test_data = np.c_[test_data, prediction]
    linear_regression(data, reg_target, test_data, test_target)


def xgboost(data, target, test_data, test_target, features=None):
    n = 406
    print ('n = ' + str(n))
    model = XGBClassifier()
    model.fit(data, target)
    prediction = model.predict(test_data)
    cv_score = cross_val_score(model, data, target, cv=10, scoring=scorer)
    # print(prediction)
    # print(test_target)
    print ('F1 score = ' + str(cv_score.mean()))
    print ('F1 score std = ' + str(cv_score.std()))
    # Feature importances into a dataframe
    if features is not None:
        feature_importances = pd.DataFrame({'feature': features, 'importance': model.feature_importances_})
        # print(feature_importances.head())
    validation.cal_rmse(prediction, test_target)


def gradient_boosting(data, target, test_data, test_target):
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=24, random_state=0)
    model.fit(data, target)
    prediction = model.predict(test_data)
    cv_score = cross_val_score(model, data, target, cv=10, scoring=scorer)
    # print(prediction)
    # print(test_target)
    print ('F1 score = ' + str(cv_score.mean()))
    print ('F1 score std = ' + str(cv_score.std()))
    return validation.cal_rmse(prediction, test_target)


def linear_regression(data, target, test_data, test_target):
    model = LinearRegression()
    model.fit(data, target)
    prediction = model.predict(test_data)
    return validation.cal_rmse(prediction, test_target)


def logistic_regression(data, target, test_data, test_target):
    model = LogisticRegression()
    model.fit(data, target)
    prediction = model.predict(test_data)
    return validation.cal_rmse(prediction, test_target)


def kneighbors(data, target, test_data, test_target):
    model = KNeighborsClassifier()
    model.fit(data, target)
    prediction = model.predict(test_data)
    return validation.cal_rmse(prediction, test_target)


def kneighbors_reg(data, target, test_data, test_target):
    model = KNeighborsRegressor()
    model.fit(data, target)
    prediction = model.predict(test_data)
    return validation.cal_rmse(prediction, test_target)


def decision_tree_reg(data, target, test_data, test_target):
    model = DecisionTreeRegressor()
    model.fit(data, target)
    prediction = model.predict(test_data)
    cv_score = cross_val_score(model, data, target, cv=10, scoring=scorer)
    # print(prediction)
    # print(test_target)
    print ('F1 score = ' + str(cv_score.mean()))
    print ('F1 score std = ' + str(cv_score.std()))
    return validation.cal_rmse(prediction, test_target)
