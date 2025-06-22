import xgboost as xgb
from xgboost import XGBClassifier
import pandas as pd
import joblib
from typing import Any
from typing import Tuple
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.preprocessing import LabelEncoder
import os


def train(X: pd.DataFrame, y: pd.Series, model_name:str) -> Tuple[XGBClassifier, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:

        # train, val, test split - first take 60% for train, then split temp file in half for validation and test data
        X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, stratify=y, random_state=42)

        # split validation in half for train and test
        X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)

        # initialize model
        model = XGBClassifier(
            n_estimators=1000,
            early_stopping_rounds=10,
            eval_metric= 'mlogloss',              # multiclass log loss
            learning_rate=0.1, 
            max_depth=3,
            random_state=42                          
        )  # for classification

        # fit model
        model.fit(
            X_train,
            y_train,
            eval_set=[(X_val, y_val)],
            verbose=False
        )

        model_path = os.path.join('models', model_name)
        joblib.dump(model, model_path)

        return model, X_train, y_train, X_val, y_val, X_test, y_test
