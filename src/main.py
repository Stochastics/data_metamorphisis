import pandas as pd
import yfinance as yf
import requests
import matplotlib.pyplot as plt
import yaml
import os
from dotenv import load_dotenv
from data_fetcher import fetch_fred_data
from data_processor import calculate_percentage_changes
from plotter import plot_cpi_changes, plot_stock_prices

# Load environment variables from .env file
load_dotenv()

# Load configuration
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

# Extract configuration
cpi_series_id = config['cpi_series_id']
treasury_yield_series_id = config['treasury_yield_series_id']
tickers = config['tickers']
start_date = config['start_date']
end_date = config['end_date']

def main():
    # Fetch CPI data
    cpi_df = fetch_fred_data(cpi_series_id, start_date, end_date)
    if not cpi_df.empty:
        inflation_df = calculate_percentage_changes(cpi_df, value_column='value', change_types=['mom', 'yoy'])
        if not inflation_df.empty:
            inflation_df.to_csv('output/inflation_data.csv', columns=['monthly_inflation_rate', 'yoy_inflation_rate'])
            print('Inflation data saved to inflation_data.csv')
            plot_cpi_changes(inflation_df)
        else:
            print('No inflation data to save.')
    else:
        print('No CPI data to process.')

    # Fetch Treasury yield data
    treasury_yield_df = fetch_fred_data(treasury_yield_series_id, start_date, end_date)
    if not treasury_yield_df.empty:
        treasury_yield_df.to_csv('output/30_year_treasury_yield.csv', columns=['value'])
        print('30-year Treasury yield data saved to 30_year_treasury_yield.csv')
        plt.figure(figsize=(12, 6))
        plt.plot(treasury_yield_df.index, treasury_yield_df['value'], label='30-Year Treasury Yield', color='purple')
        plt.title('30-Year Treasury Yield Over Time')
        plt.xlabel('Date')
        plt.ylabel('Yield (%)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('output/30_year_treasury_yield.png')
        plt.show()

    # Fetch daily stock data
    stock_data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        if not df.empty:
            df.reset_index(inplace=True)
            df.set_index('Date', inplace=True)
            stock_data[ticker] = df
            print(f"Data for {ticker} fetched successfully.")
        else:
            print(f"No data found for ticker {ticker}.")
    
    plot_stock_prices(stock_data)

if __name__ == "__main__":
    main()
