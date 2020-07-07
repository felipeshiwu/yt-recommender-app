import pandas as pd
import re
import joblib as jb
from scipy.sparse import hstack, csr_matrix
import numpy as np
import json

mdl_rf = jb.load("mlrandom_forest_20200420.pkl.z")
mdl_lr = jb.load("mllogistic_reg_20200420.pkl.z")
mdl_lgbm = jb.load("mllgbm_20200420.pkl.z")
title_vec = jb.load("title_vectorizer_20200420.pkl.z")

def compute_features(data):
    publish_date = pd.to_datetime(data['upload_date'])

    views = data['view_count']
    title = data['title']

    features = dict()

    features['tempo_desde_pub'] = (pd.Timestamp.today() - publish_date) / np.timedelta64(1, 'D')
    features['views'] = views
    features['views_por_dia'] = features['views'] / features['tempo_desde_pub']
    del features['tempo_desde_pub']

    vectorized_title = title_vec.transform([title])

    num_features = csr_matrix(np.array([features['views'], features['views_por_dia']]))
    feature_array = hstack([num_features, vectorized_title])

    return feature_array


def compute_prediction(data):
    feature_array = compute_features(data)
    print(feature_array)

    if feature_array is None:
        return 0


    p_rf = mdl_rf.predict_proba(feature_array)[0][1]
    p_lr = mdl_lr.predict_proba(feature_array)[0][1]
    p_lgbm = mdl_lgbm.predict_proba(feature_array)[0][1]

    p = (p_rf + p_lgbm + p_lr)/3
    #log_data(data, feature_array, p)

    return p

