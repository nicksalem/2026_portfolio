from typing import Tuple
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def preprocessor(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series, LabelEncoder]:

    #remove players with less than 50 games
    df50 = df[df['G'] >=50].copy()

    #select dtypes = numeric
    df50_numeric = df50.select_dtypes('number').drop(columns=['Age', 'Year'])

    # Label encode the column
    le = LabelEncoder()
    df50['Pos_encoded'] = le.fit_transform(df50['Pos'])

    # Features and target
    X = df50_numeric.copy()
    y = df50['Pos_encoded'].copy()

    return X,y,le