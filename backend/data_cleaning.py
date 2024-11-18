# Handles missing values, outlier removal, normalization, and conversion to numeric.
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def handle_missing_values(df):
    for column in df.columns:
        if df[column].dtype in ['float64', 'int64']:
            df[column] = df[column].fillna(df[column].median())
        else:
            df[column] = df[column].fillna(df[column].mode()[0])
    return df

def remove_outliers(df):
    numeric_cols = df.select_dtypes(include=[np.number])
    Q1 = numeric_cols.quantile(0.25)
    Q3 = numeric_cols.quantile(0.75)
    IQR = Q3 - Q1
    outliers = (numeric_cols < (Q1 - 1.5 * IQR)) | (numeric_cols > (Q3 + 1.5 * IQR))
    df = df[~outliers.any(axis=1)]
    return df

def normalize_data(df, exclude_columns=[]):
    scaler = MinMaxScaler()
    numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns.difference(exclude_columns)
    df[numerical_columns] = scaler.fit_transform(df[numerical_columns])
    return df

def convert_to_numeric(df):
    for column in df.columns:
        if column != "Year":
            df[column] = pd.to_numeric(df[column], errors='coerce')
    df.fillna(df.median(numeric_only=True), inplace=True)
    return df
