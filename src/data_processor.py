import pandas as pd

def calculate_percentage_changes(df, value_column, change_types=['mom', 'yoy']):
    result_df = df.copy()
    
    if 'mom' in change_types:
        result_df['monthly_inflation_rate'] = result_df[value_column].pct_change() * 100
        result_df['monthly_inflation_rate'] = result_df['monthly_inflation_rate'].round(2)
    
    if 'yoy' in change_types:
        result_df['yoy_inflation_rate'] = result_df[value_column].pct_change(periods=12) * 100
        result_df['yoy_inflation_rate'] = result_df['yoy_inflation_rate'].round(2)
    
    return result_df.dropna()
