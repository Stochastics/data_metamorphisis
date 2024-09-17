import pandas as pd
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

# Extract configuration
econ_data = config['econ_data']
tickers = config['tickers']
start_date = config['start_date']
end_date = config['end_date']

def apply_transformations(df, transforms):
    """
    Applies a sequence of transformations to the dataframe.
    Returns only the transformed columns.
    """
    transformed_columns = []  # Track transformed columns
    for transform in transforms:
        if transform == 'mom_percentage_change' or transform == 'yoy_percentage_change':
            df = calculate_percentage_changes(df, value_column='value', change_types=transforms)
            transformed_columns.extend([col for col in df.columns if col.endswith('percentage_change')])
    
    # Return only the columns that were successfully created
    return df[[col for col in transformed_columns if col in df.columns]]

def main():
    # Fetch and process economic data
    for econ_entry in econ_data:
        series_id = econ_entry['series_id']
        transforms = econ_entry.get('transforms', [])

        # Fetch data from FRED
        econ_df = fetch_fred_data(series_id, start_date, end_date)
        print(econ_df.head(10))
        if not econ_df.empty:
            # Filter out None values from transforms
            valid_transforms = [t for t in transforms if t and t != 'None']
            if valid_transforms:
                econ_df = apply_transformations(econ_df, valid_transforms)
            print(f"Transformed data for {series_id}:")
            print(econ_df.head(10))
            econ_df.to_csv(f'output/{series_id}_data.csv')
            print(f'Economic data for {series_id} saved to {series_id}_data.csv')
            plot_econ_data(econ_df, title=f'Economic Data for {series_id} Over Time', y_label='Value')

    # Fetch stock data and apply transformations
    stock_data = {}
    for ticker_entry in tickers:
        symbol = ticker_entry['symbol']
        transforms = ticker_entry.get('transforms', [])

        # Fetch stock data using yfinance
        stock_df = yf.download(symbol, start=start_date, end=end_date)

        if not stock_df.empty:
            # Filter out None values from transforms
            valid_transforms = [t for t in transforms if t and t != 'None']
            if valid_transforms:
                stock_df = apply_transformations(stock_df, valid_transforms)
                print("############## APPLIED TRANSFORMATIONS ###################")
            stock_data[symbol] = stock_df
            print(f'Data for {symbol} added to stock_data.')
        else:
            print(f'No data found for symbol {symbol}.')
    
    for symbol, df in stock_data.items():
        print(f"Data for {symbol}:")
        print(df.head())  # Display the first few rows of each DataFrame
        
    plot_stock_prices(stock_data)

if __name__ == "__main__":
    main()