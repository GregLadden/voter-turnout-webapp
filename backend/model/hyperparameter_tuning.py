
from sklearn.model_selection import GridSearchCV

def perform_grid_search(estimator, param_grid, X_train, y_train, cv=5, scoring='neg_mean_squared_error', n_jobs=-1):
    """
    Performs GridSearchCV for hyperparameter tuning.

    Args:
        estimator: The model to tune (e.g., RandomForestRegressor, LinearRegression).
        param_grid (dict): The hyperparameter grid to search.
        X_train: Training features.
        y_train: Training labels.
        cv (int): Number of cross-validation folds (default=5).
        scoring (str): Scoring metric for optimization (default='neg_mean_squared_error').
        n_jobs (int): Number of parallel jobs to run (default=-1 for all available cores).

    Returns:
        best_model: The model with the best hyperparameters.
        best_params (dict): The best hyperparameters found during the search.
    """
    grid_search = GridSearchCV(
        estimator=estimator,
        param_grid=param_grid,
        cv=cv,
        scoring=scoring,
        n_jobs=n_jobs
    )
    grid_search.fit(X_train, y_train)

    return grid_search.best_estimator_, grid_search.best_params_
