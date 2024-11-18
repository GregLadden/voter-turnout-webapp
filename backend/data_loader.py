import pandas as pd
import seaborn as sns

# Set visual style for plots
sns.set(style="whitegrid")

def load_data(url="https://raw.githubusercontent.com/drewmayberry11/Machine_Learning_Data_Sets/main/voter_turnout_project5.csv"):
    # Specify the decimal parameter to handle commas as decimal points
    voter_data = pd.read_csv(url, decimal=',', skipinitialspace=True)
    return voter_data
