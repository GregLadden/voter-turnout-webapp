
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from data_loader import load_data
from data_cleaning import handle_missing_values, remove_outliers, normalize_data, convert_to_numeric
from feature_engineering import create_meaningful_features
from model_training import (train_random_forest, evaluate_model, feature_importance,
                            cross_validate_model, tune_hyperparameters)
from sklearn.model_selection import train_test_split
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load data globally
voter_data = load_data()

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Load the data
        voter_data = load_data()

        # Replace NaN values with None to make JSON-compliant
        voter_data = voter_data.where(pd.notnull(voter_data), None)

        # Convert the DataFrame to a dictionary to send as JSON
        data = voter_data.to_dict(orient="records")
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clean-data', methods=['GET'])
def clean_data():
    global voter_data

    # Optional query parameters to control each cleaning step
    handle_missing_flag = request.args.get('handle_missing', 'true').lower() == 'true'
    remove_outliers_flag = request.args.get('remove_outliers', 'true').lower() == 'true'
    normalize_flag = request.args.get('normalize', 'true').lower() == 'true'
    convert_numeric_flag = request.args.get('convert_numeric', 'true').lower() == 'true'

    # Apply cleaning steps based on parameters
    if handle_missing_flag:
        voter_data = handle_missing_values(voter_data)
    if remove_outliers_flag:
        voter_data = remove_outliers(voter_data)
    if normalize_flag:
        voter_data = normalize_data(voter_data, exclude_columns=['Year'])
    if convert_numeric_flag:
        voter_data = convert_to_numeric(voter_data)

    # Round numeric values to 2 decimal places for readability
    voter_data = voter_data.applymap(lambda x: round(x, 2) if isinstance(x, float) else x)

    # Convert the DataFrame to JSON for the response
    data = voter_data.to_dict(orient="records")
    return jsonify(data)

@app.route('/missing-values', methods=['GET'])
def handle_missing_values_route():
    global voter_data
    voter_data = handle_missing_values(voter_data)
    return jsonify({"message": "Missing values handled."})

@app.route('/remove-outliers', methods=['GET'])
def remove_outliers_route():
    global voter_data
    voter_data = remove_outliers(voter_data)
    return jsonify({"message": "Outliers removed."})

@app.route('/normalize', methods=['GET'])
def normalize_data_route():
    global voter_data
    voter_data = normalize_data(voter_data, exclude_columns=['Year'])
    return jsonify({"message": "Data normalized."})

@app.route('/convert-to-numeric', methods=['GET'])
def convert_to_numeric_route():
    global voter_data
    voter_data = convert_to_numeric(voter_data)
    return jsonify({"message": "Data converted to numeric."})

@app.route('/feature-engineering', methods=['GET'])
def feature_engineering_route():
    global voter_data
    voter_data = create_meaningful_features(voter_data)
    return jsonify({"message": "Feature engineering applied."})

@app.route('/train-random-forest', methods=['POST'])
def train_random_forest_route():
    global voter_data
    target = 'Total Voter Turnout'
    features = request.json.get('features', [])
    X = voter_data[features]
    y = voter_data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_random_forest(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    return jsonify(metrics)

@app.route('/feature-importance', methods=['POST'])
def feature_importance_route():
    global voter_data
    features = request.json.get('features', [])
    target = 'Total Voter Turnout'
    X = voter_data[features]
    y = voter_data[target]
    model = train_random_forest(X, y)
    importance = feature_importance(model, features).to_dict(orient="records")
    return jsonify(importance)

@app.route('/cross-validation', methods=['POST'])
def cross_validation_route():
    global voter_data
    features = request.json.get('features', [])
    target = 'Total Voter Turnout'
    X = voter_data[features]
    y = voter_data[target]
    model = train_random_forest(X, y)
    cv_scores = cross_validate_model(model, X, y).tolist()
    return jsonify({"cross_validation_rmse_scores": cv_scores, "mean_rmse": float(np.mean(cv_scores))})

@app.route('/tune-random-forest', methods=['POST'])
def tune_random_forest_route():
    global voter_data
    features = request.json.get('features', [])
    target = 'Total Voter Turnout'
    X = voter_data[features]
    y = voter_data[target]
    _, best_params = tune_hyperparameters(X, y)
    return jsonify({"best_params": best_params})

if __name__ == "__main__":
    app.run(debug=True)

