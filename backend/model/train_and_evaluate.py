from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def train_and_evaluate_model(model, X_train, X_test, y_train, y_test):
    """
    Trains the given model and evaluates it on the test set.

    Args:
        model: The model to train.
        X_train, X_test, y_train, y_test: The train-test split of the dataset.

    Returns:
        A dictionary of evaluation metrics (MAE, MSE, RMSE, R²).
    """
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    metrics = {
        "mae": round(mean_absolute_error(y_test, y_pred), 2),
        "mse": round(mean_squared_error(y_test, y_pred), 2),
        "rmse": round(np.sqrt(mean_squared_error(y_test, y_pred)), 2),
        "r2": round(r2_score(y_test, y_pred), 2)
    }

    return metrics
