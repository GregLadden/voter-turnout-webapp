from sklearn.ensemble import RandomForestRegressor

def train_random_forest(X_train, y_train, n_estimators=100, random_state=42):
    """
    Train a Random Forest Regressor model on the training data.
    
    Parameters:
        X_train (pd.DataFrame): Training features.
        y_train (pd.Series): Training target values.
        n_estimators (int): Number of trees in the forest.
        random_state (int): Seed for reproducibility.
        
    Returns:
        RandomForestRegressor: The trained Random Forest model.
    """
    rf_model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    rf_model.fit(X_train, y_train)
    return rf_model

