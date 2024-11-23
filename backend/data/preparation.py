from sklearn.model_selection import train_test_split

def define_features_and_target(voter_data):
    """
    Define the features and target for the model.
    
    Parameters:
        voter_data (pd.DataFrame): The voter data containing all columns.
        
    Returns:
        tuple: A tuple containing the features list and target variable name.
    """
    target = 'Total Voter Turnout'
    features = [
        'White', 'Black', 'Hispanic', 'Asian',  # Racial/Ethnic groups
        'Male', 'Female',  # Gender groups
        '18 to 24', '22 to 44', '45 to 64', '65 and Over',  # Age groups
        'Gender_Gap',  # Difference in turnout between females and males
        'White_Black_Gap', 'White_Hispanic_Gap',  # Racial turnout gaps
        'Youth_Senior_Gap',  # Difference in turnout between youngest and oldest age groups
        'Population_Growth'  # Year-over-year population growth percentage
    ]
    return features, target


def split_dataset(voter_data, features, target, test_size=0.2, random_state=42):
    """
    Split the dataset into training and testing sets.
    
    Parameters:
        voter_data (pd.DataFrame): The voter data containing features and the target variable.
        features (list): List of feature column names.
        target (str): The target variable column name.
        test_size (float): Proportion of the dataset for testing.
        random_state (int): Seed for random splitting.
        
    Returns:
        dict: Dictionary with training and testing data splits:
              - 'X_train': Training features
              - 'X_test': Testing features
              - 'y_train': Training target
              - 'y_test': Testing target
    """
    print(features)
    print(target)
    X = voter_data[features]
    y = voter_data[target]
    print(X)
    print(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    print(X_train)
    print(X_test)
    print(y_train)
    print(y_test)
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test
    }

