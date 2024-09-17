import pandas as pd

def calculate_percentage_changes(df, value_column, change_types):
    """
    Adds percentage changes (MoM, YoY) to the DataFrame based on the specified change types.
    """
    if 'mom_percentage_change' in change_types:
        df['mom_percentage_change'] = df[value_column].pct_change() * 100
        print("Month-over-Month percentage change:")
        print(df[['mom_percentage_change']].head(20))  # Print to verify

    if 'yoy_percentage_change' in change_types:
        df = df.sort_index()  # Sort by index if it's a date index
        df['yoy_percentage_change'] = df[value_column].pct_change(periods=12) * 100
        print("Year-over-Year percentage change:")
        print(df[['yoy_percentage_change']].head(20))  # Print to verify

    return df

def normalize_data(df, value_column, column_name='normalized'):
    """
    Normalize a column of data to the range 0-1.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        value_column (str): The column to normalize.
        column_name (str): The name of the output normalized column.

    Returns:
        pd.DataFrame: Dataframe with the normalized column.
    """
    result_df = df.copy()
    result_df[column_name] = (result_df[value_column] - result_df[value_column].min()) / (result_df[value_column].max() - result_df[value_column].min())
    return result_df

def log_transform(df, value_column, column_name='log_transformed'):
    """
    Apply a log transformation to a column.

    Args:
        df (pd.DataFrame): The dataframe containing the data.
        value_column (str): The column to apply the log transformation to.
        column_name (str): The name of the output log-transformed column.

    Returns:
        pd.DataFrame: Dataframe with the log-transformed column.
    """
    result_df = df.copy()
    result_df[column_name] = result_df[value_column].apply(lambda x: np.log(x) if x > 0 else None)
    return result_df.dropna()
