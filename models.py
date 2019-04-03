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
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_score
import validation
import pandas as pd

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
    model = RandomForestClassifier(n_estimators=400, random_state=10, n_jobs=-1)
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
        print(feature_importances.head())
    return validation.cal_rmse(prediction, test_target)


def gradient_boosting(data, target, test_data, test_target):
    model = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=24, random_state=0)
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
