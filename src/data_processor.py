import polars as pl

def calculate_percentage_changes(df, value_column='value', change_types=['mom', 'yoy']):
    if value_column not in df.columns:
        return df  # Return the original DataFrame if the column isn't found

    # Calculate month-over-month percentage change
    if 'mom' in change_types:
        df = df.with_columns(
            ((pl.col(value_column) - pl.col(value_column).shift(1)) / pl.col(value_column).shift(1) * 100)
            .alias('monthly_inflation_rate')
        )

    # Calculate year-over-year percentage change
    if 'yoy' in change_types:
        df = df.with_columns(
            ((pl.col(value_column) - pl.col(value_column).shift(12)) / pl.col(value_column).shift(12) * 100)
            .alias('yoy_inflation_rate')
        )

    return df

def normalize_data(df, value_column, column_name='normalized'):
    result_df = df.with_columns([
        ((pl.col(value_column) - pl.col(value_column).min()) / 
         (pl.col(value_column).max() - pl.col(value_column).min())).alias(column_name)
    ])
    return result_df

def log_transform(df, value_column, column_name='log_transformed'):
    result_df = df.with_column(
        pl.when(pl.col(value_column) > 0)
          .then(pl.col(value_column).log())
          .otherwise(None).alias(column_name)
    )
    return result_df.drop_nulls()
