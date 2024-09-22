import polars as pl
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import yaml
import os
from dotenv import load_dotenv
from data_fetcher import fetch_fred_data
from data_processor import calculate_percentage_changes, normalize_data, log_transform
from plotter import plot_econ_data, plot_stock_prices

# Load environment variables from .env file
load_dotenv()

# Load configuration
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
    print("Loaded config:", config)

# Extract configuration
econ_data = config['econ_data']
tickers = config['tickers']
start_date = config['start_date']
end_date = config['end_date']

def apply_transformations(df, transforms, value_column):
    """
    Applies a sequence of transformations to the dataframe.
    Replaces the specified value column with the transformed data.
    """
    for transform in transforms:
        print(f"Applying transform: {transform}")

        if value_column not in df.columns:
            print(f"Warning: '{value_column}' column not found in the DataFrame.")
            continue

        if transform == 'identity':
            continue
        elif transform == 'mom_percentage_change':
            df = calculate_percentage_changes(df, value_column=value_column, change_types=['mom'])
        elif transform == 'yoy_percentage_change':
            df = calculate_percentage_changes(df, value_column=value_column, change_types=['yoy'])
        elif transform == 'log':
            df = log_transform(df, value_column=value_column)
        elif transform == 'normalize':
            df = normalize_data(df, value_column=value_column)
        else:
            print(f"Warning: Unknown transform '{transform}' for series.")
            continue

        # Update the value column to the last transformed column
        last_transformed_col = df.columns[-1]
        df = df.with_columns(pl.col(last_transformed_col).alias(value_column))

        # Print DataFrame shape and head for verification
        print(f"Transformed DataFrame shape: {df.shape}")
        print(df.head())

    return df

def main():
    # Fetch and process economic data
    for econ_entry in econ_data:
        series_id = econ_entry['series_id']
        value_column = econ_entry.get('value_column', 'value')  # Default to 'value'
        plot_title = econ_entry.get('plot_title','None')
        print(f"Now running series {series_id}")
        transforms = econ_entry.get('transforms', ['identity'])

        # Fetch data from FRED
        econ_df = fetch_fred_data(series_id, start_date, end_date)
        if not econ_df.is_empty():
            # Apply transformations
            econ_df = apply_transformations(econ_df, transforms, value_column)
            econ_df.write_csv(f'output/{series_id}_data.csv')
            plot_econ_data(econ_df, plot_title , y_label='Value')


    for ticker_entry in tickers:
        symbol = ticker_entry['symbol']
        transforms = ticker_entry.get('transforms', ['identity'])
        plot_title = ticker_entry.get('plot_title','None')
        value_column = ticker_entry.get('value_column', 'value') 
        # Download stock data
        stock_df = yf.download(symbol, start=start_date, end=end_date)
        print(stock_df.head(10))
        if not stock_df.empty:
            # Convert to Polars DataFrame
            stock_df = pl.DataFrame(stock_df.reset_index())
            stock_df = apply_transformations(stock_df, transforms, value_column)
            plot_stock_prices(stock_df, value_column, plot_title)


if __name__ == "__main__":
    main()
