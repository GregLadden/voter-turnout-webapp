from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from data.loader import load_data
from model.train_randomForest import  (train_random_forest_model, hyper_tune_random_forest) 
from model.train_linearRegression import (train_linear_regression_model, hyper_tune_linear_regression)


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Load data globally
voter_data = load_data()

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Load the data
        voter_data = load_data()
        
        # Strip any leading/trailing spaces in column names
        voter_data.columns = voter_data.columns.str.strip()

        # Replace NaN values with None to make JSON-compliant
        voter_data = voter_data.where(pd.notnull(voter_data), None)

        # Convert the DataFrame to a dictionary to send as JSON
        data = voter_data.to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/train-randomforest', methods=['POST'])
def train_random_forest():
    try:
        # Train the Random Forest model and get metrics
        _, metrics = train_random_forest_model(voter_data)

        # Return success message and metrics
        return jsonify({
            "message": "Random Forest model trained successfully",
            "metrics": metrics
        }), 200

    except KeyError as e:
        return jsonify({"error": f"KeyError: Missing or incorrect column name - {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"ValueError: Invalid data or parameters - {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



@app.route('/hyperparameter-tuning-randomforest', methods=['POST'])
def hyper_tune_random_forest_api():
    try:
        # Define hyperparameter grid
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2]
        }

        # Perform hyperparameter tuning and evaluation
        _, metrics, best_params = hyper_tune_random_forest(voter_data, param_grid)

        # Return success message, metrics, and best parameters
        return jsonify({
            "message": "Random Forest model trained and tuned successfully",
            "best_params": best_params,
            "metrics": metrics
        }), 200

    except KeyError as e:
        return jsonify({"error": f"KeyError: Missing or incorrect column name - {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"ValueError: Invalid data or parameters - {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/train-linear-regression', methods=['POST'])
def train_linear_regression():
    try:
        # Train the Linear Regression model and get metrics
        _, metrics = train_linear_regression_model(voter_data)

        # Return success message and metrics
        return jsonify({
            "message": "Linear Regression model trained successfully",
            "metrics": metrics
        }), 200

    except KeyError as e:
        return jsonify({"error": f"KeyError: Missing or incorrect column name - {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"ValueError: Invalid data or parameters - {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/hyperparameter-tuning-linear', methods=['POST'])
def hyper_tune_linear_regression_api():
    try:
        # Define hyperparameter grid for Lasso Regression
        param_grid = {
            'alpha': [0.01, 0.1, 1, 10],  # Regularization strength
            'fit_intercept': [True, False]
        }

        # Perform hyperparameter tuning and evaluation
        _, metrics, best_params = hyper_tune_linear_regression(voter_data, param_grid)

        # Return success message, metrics, and best parameters
        return jsonify({
            "message": "Linear Regression (Lasso) model trained and tuned successfully",
            "best_params": best_params,
            "metrics": metrics
        }), 200

    except KeyError as e:
        return jsonify({"error": f"KeyError: Missing or incorrect column name - {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"ValueError: Invalid data or parameters - {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        print("linear data: ", data)
        selected_columns = data.get('columns', [])  # List of column headers to predict for
        predict_years = data.get('predict_years')

        if not selected_columns or not isinstance(selected_columns, list):
            return jsonify({"error": "Invalid or missing 'columns' parameter"}), 400
        if not predict_years:
            return jsonify({"error": "Missing 'predict_years' parameter"}), 400

        # Combine years from the dataset and prediction years
        min_year = voter_data['Year'].min()
        max_year = max(predict_years)
        full_years = np.arange(min_year, max_year + 1).tolist()  # Start from the earliest year in data

        predictions = {}
        actual_data = {}
        metrics = {}

        for column in selected_columns:
            if column not in voter_data.columns:
                return jsonify({"error": f"Invalid column '{column}'"}), 400

            # Extract actual data
            valid_data = voter_data[['Year', column]].dropna()
            actual_values = valid_data[column].values
            actual_years = valid_data['Year'].values.tolist()

            # Train and predict
            model = LinearRegression()
            model.fit(valid_data['Year'].values.reshape(-1, 1), actual_values)
            predicted_values = model.predict(np.array(full_years).reshape(-1, 1)).tolist()

            # Calculate metrics
            metrics[column] = {
                "mae": float(mean_absolute_error(actual_values, model.predict(valid_data['Year'].values.reshape(-1, 1)))),
                "r2": float(r2_score(actual_values, model.predict(valid_data['Year'].values.reshape(-1, 1)))),
            }

            predictions[column] = predicted_values
            actual_data[column] = {
                "years": actual_years,
                "values": actual_values.tolist()
            }

        # Return predictions, actual data, and metrics
        return jsonify({
            "message": "Prediction successful",
            "predictions": predictions,
            "actual_data": actual_data,
            "metrics": metrics,
            "years": full_years
        }), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/predict-randomforest', methods=['POST'])
def predict_random_forest():
    try:
        data = request.json
        print("random-forest data", data)
        
        # Sanitize user inputs
        selected_columns = [col.strip() for col in data.get('columns', [])]  # Remove extra whitespace
        predict_years = data.get('predict_years')

        # Validate inputs
        if not selected_columns or not isinstance(selected_columns, list):
            return jsonify({"error": "Invalid or missing 'columns' parameter"}), 400
        if not predict_years:
            return jsonify({"error": "Missing 'predict_years' parameter"}), 400

        # Clean column names in the dataset
        voter_data.columns = voter_data.columns.str.strip()  # Strip whitespace from column names

        # Combine years from the dataset and prediction years
        min_year = voter_data['Year'].min()
        max_year = max(predict_years)
        full_years = np.arange(min_year, max_year + 1).tolist()

        predictions = {}
        actual_data = {}
        metrics = {}

        for column in selected_columns:
            if column not in voter_data.columns:
                return jsonify({"error": f"Invalid column '{column}'"}), 400

            # Align Year and column data
            valid_data = voter_data[['Year', column]].dropna()
            actual_values = valid_data[column].values
            actual_years = valid_data['Year'].values.tolist()

            # Train and predict using Random Forest
            model = RandomForestRegressor(random_state=42, n_estimators=100)
            model.fit(valid_data['Year'].values.reshape(-1, 1), actual_values)
            predicted_values = model.predict(np.array(full_years).reshape(-1, 1)).tolist()

            # Calculate metrics
            metrics[column] = {
                "mae": float(mean_absolute_error(actual_values, model.predict(valid_data['Year'].values.reshape(-1, 1)))),
                "r2": float(r2_score(actual_values, model.predict(valid_data['Year'].values.reshape(-1, 1)))),
            }

            predictions[column] = predicted_values
            actual_data[column] = {
                "years": actual_years,
                "values": actual_values.tolist()
            }

        # Return predictions, actual data, and metrics
        return jsonify({
            "message": "Prediction successful",
            "predictions": predictions,
            "actual_data": actual_data,
            "metrics": metrics,
            "years": full_years
        }), 200

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500




@app.route('/columns', methods=['GET'])
def get_columns():
    try:
        # Assuming voter_data is a Pandas DataFrame
        columns = voter_data.columns.tolist()  # Extract column names
        return jsonify({"columns": columns}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)


