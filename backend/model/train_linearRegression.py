from model.utils import clean_and_prepare_data
from model.train_and_evaluate import train_and_evaluate_model
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from model.hyperparameter_tuning import perform_grid_search
from sklearn.linear_model import Lasso

def train_linear_regression_model(data):
    """
    Trains and evaluates a Linear Regression model.

    Args:
        data (DataFrame): The dataset to train and evaluate the model on.

    Returns:
        model: Trained Linear Regression model.
        metrics (dict): Evaluation metrics of the model.
    """
    # Prepare the data
    X_train, X_test, y_train, y_test = clean_and_prepare_data(data, exclude_columns=['Year'])

    # Scale the data for Linear Regression
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train and evaluate the Linear Regression model
    model = LinearRegression()
    metrics = train_and_evaluate_model(model, X_train_scaled, X_test_scaled, y_train, y_test)

    return model, metrics

def hyper_tune_linear_regression(data, param_grid):
    """
    Tunes a Linear Regression (Lasso) model using GridSearchCV and evaluates it.

    Args:
        data (DataFrame): The dataset to train and tune the model on.
        param_grid (dict): Hyperparameter grid for tuning.

    Returns:
        best_model: The best Linear Regression (Lasso) model found by GridSearchCV.
        metrics (dict): Evaluation metrics of the best model.
        best_params (dict): The best hyperparameters found by GridSearchCV.
    """
    # Prepare the data
    X_train, X_test, y_train, y_test = clean_and_prepare_data(data, exclude_columns=['Year'])

    # Scale the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Perform GridSearchCV
    best_lasso_model, best_params = perform_grid_search(
        estimator=Lasso(random_state=42),
        param_grid=param_grid,
        X_train=X_train_scaled,
        y_train=y_train
    )

    # Evaluate the tuned model
    metrics = train_and_evaluate_model(best_lasso_model, X_train_scaled, X_test_scaled, y_train, y_test)

    return best_lasso_model, metrics, best_params
