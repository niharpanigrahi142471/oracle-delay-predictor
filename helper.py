import pandas as pd

def analyze_delay(df):
    df['Delay Risk'] = df.apply(lambda row: "High" if (
        row['Planned Duration'] > row['Actual Duration'] and
        row['Dependencies'] > 3 and
        row['Project Phase'] in ['Testing', 'Deployment']
    ) else "Low", axis=1)

    return df[['Task Name', 'Planned Duration', 'Actual Duration', 'Dependencies', 'Project Phase', 'Delay Risk']]
