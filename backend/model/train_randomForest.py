from model.utils import clean_and_prepare_data
from model.hyperparameter_tuning import perform_grid_search
from model.train_and_evaluate import train_and_evaluate_model 
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def train_random_forest_model(data):
    # Prepare the data
    X_train, X_test, y_train, y_test = clean_and_prepare_data(data, exclude_columns=['Year'])

    # Train the Random Forest model
    rf_model = RandomForestRegressor(random_state=42)
    rf_model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = rf_model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    metrics = {
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2": round(r2, 2)
    }

    print(f"Random Forest - MAE: {mae:.2f}, RMSE: {rmse:.2f}, R²: {r2:.2f}")
    return rf_model, metrics

def hyper_tune_random_forest(data, param_grid):
    """
    Tunes a Random Forest model using GridSearchCV and evaluates it.

    Args:
        data (DataFrame): The dataset to train and tune the model on.
        param_grid (dict): Hyperparameter grid for tuning.

    Returns:
        best_model: The best Random Forest model found by GridSearchCV.
        metrics (dict): Evaluation metrics of the best model.
        best_params (dict): The best hyperparameters found by GridSearchCV.
    """
    # Prepare the data
    X_train, X_test, y_train, y_test = clean_and_prepare_data(data, exclude_columns=['Year'])

    # Perform GridSearchCV
    best_rf_model, best_params = perform_grid_search(
        estimator=RandomForestRegressor(random_state=42),
        param_grid=param_grid,
        X_train=X_train,
        y_train=y_train
    )

    # Evaluate the tuned model
    metrics = train_and_evaluate_model(best_rf_model, X_train, X_test, y_train, y_test)

    return best_rf_model, metrics, best_params
