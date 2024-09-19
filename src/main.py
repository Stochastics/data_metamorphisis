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
    Returns the transformed dataframe.
    """
    for transform in transforms:
        if transform == 'identity':
            # Identity transform does nothing
            continue
        elif transform == 'mom_percentage_change':
            # Calculate month-over-month percentage change
            df = calculate_percentage_changes(df, value_column='value', change_types=['mom_percentage_change'])
        elif transform == 'yoy_percentage_change':
            # Calculate year-over-year percentage change
            df = calculate_percentage_changes(df, value_column='value', change_types=['yoy_percentage_change'])
        elif transform == 'log':
            # Apply log transformation
            df = log_transform(df, value_column='value')
        elif transform == 'normalize':
            # Normalize data
            df = normalize_data(df, value_column='value')
    
    return df

def main():
    # Fetch and process economic data
    for econ_entry in econ_data:
        series_id = econ_entry['series_id']
        print(f"Now running series{series_id}")
        transforms = econ_entry.get('transforms', ['identity'])  # Default to identity if no transform is provided

        # Fetch data from FRED
        econ_df = fetch_fred_data(series_id, start_date, end_date)
        print(econ_df.head(10))
        if not econ_df.empty:
            # Apply transformations
            econ_df = apply_transformations(econ_df, transforms)
            print(f"Transformed data for {series_id}:")
            print(econ_df.head(10))
            econ_df.to_csv(f'output/{series_id}_data.csv')
            print(f'Economic data for {series_id} saved to {series_id}_data.csv')
            plot_econ_data(econ_df, title=f'Economic Data for {series_id} Over Time', y_label='Value')

    # Fetch stock data and apply transformations
    stock_data = {}
    for ticker_entry in tickers:
        symbol = ticker_entry['symbol']
        transforms = ticker_entry.get('transforms', ['identity'])  # Default to identity if no transform is provided

        # Fetch stock data using yfinance
        stock_df = yf.download(symbol, start=start_date, end=end_date)

        if not stock_df.empty:
            # Apply transformations
            stock_df = apply_transformations(stock_df, transforms)
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
