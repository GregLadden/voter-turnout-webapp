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

    # Define lower and upper bounds for each numeric column
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Clip values to these bounds instead of removing rows
    df[numeric_cols.columns] = numeric_cols.clip(lower=lower_bound, upper=upper_bound, axis=1)
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

def add_engineered_features(df):
    # Calculate gaps and population growth
    print(df)
    df['Gender_Gap'] = df['Female'] - df['Male']
    df['White_Black_Gap'] = df['White'] - df['Black']
    df['White_Hispanic_Gap'] = df['White'] - df['Hispanic']
    df['Youth_Senior_Gap'] = df['18 to 24'] - df['65 and Over']
    df['Population_Growth'] = df['Voting Population'].pct_change().fillna(0)
    return df

