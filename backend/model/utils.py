from data.cleaning import (handle_missing_values, remove_outliers, normalize_data, convert_to_numeric, add_engineered_features)
from data.preparation import (define_features_and_target, split_dataset)

# Define a reusable function for data cleaning and preparation
def clean_and_prepare_data(data, exclude_columns=None):
    """
    Cleans and prepares the data for training and testing.

    Args:
        data (DataFrame): The input dataset.
        exclude_columns (list): Columns to exclude from normalization.

    Returns:
        X_train, X_test, y_train, y_test: The split and prepared datasets.
    """
    # Step 1: Copy data to avoid modifying the original dataset
    cleaned_data = data.copy()
    
    # Step 2: Strip column names to remove extra whitespace
    cleaned_data.columns = cleaned_data.columns.str.strip()

    # Step 3: Apply data cleaning steps
    cleaned_data = handle_missing_values(cleaned_data)
    cleaned_data = remove_outliers(cleaned_data)
    cleaned_data = normalize_data(cleaned_data, exclude_columns=exclude_columns)
    cleaned_data = convert_to_numeric(cleaned_data)
    cleaned_data = add_engineered_features(cleaned_data)

    # Step 4: Define features and target
    features, target = define_features_and_target(cleaned_data)

    # Step 5: Split the dataset into training and testing sets
    splits = split_dataset(cleaned_data, features, target)
    X_train, X_test, y_train, y_test = splits['X_train'], splits['X_test'], splits['y_train'], splits['y_test']

    return X_train, X_test, y_train, y_test
