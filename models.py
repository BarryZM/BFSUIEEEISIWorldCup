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
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
import validation

# Custom scorer for cross validation
scorer = make_scorer(f1_score, greater_is_better=True, average='macro')


def get_fitted_data_set(train_set, test_set):
    features = list(train_set.columns)

    pipeline = Pipeline([('imputer', Imputer(strategy='median')),
                         ('scaler', MinMaxScaler())])

    # Fit and transform training data
    train_set = pipeline.fit_transform(train_set)
    test_set = pipeline.transform(test_set)
    return train_set, test_set


def random_forest(data, target, test_data, test_target):
    model = RandomForestClassifier(n_estimators=100, random_state=10,
                                   n_jobs=-1)
    model.fit(data, target)
    prediction = model.predict(test_data)
    print(prediction)
    print(test_target)
    return validation.cal_rmse(prediction, test_target)


def linear_regression(data, target, test_data, test_target):
    model = LinearRegression()
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
