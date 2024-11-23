# Creates new features based on existing data.
def create_meaningful_features(df):
    df['Gender_Gap'] = df['Female'] - df['Male']
    df['White_Black_Gap'] = df['White'] - df['Black']
    df['White_Hispanic_Gap'] = df['White'] - df['Hispanic']
    df['Youth_Senior_Gap'] = df['65 and Over'] - df['18 to 24']
    df['Turnout_Change'] = df['Total Voter Turnout'] - df['Total Voter Turnout'].shift(1)
    df['Population_Growth'] = (df['Voting Population'] - df['Voting Population'].shift(1)) / df['Voting Population'].shift(1) * 100
    return df
