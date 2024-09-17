import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import os

def plot_econ_data(econ_df, title, y_label):
    plt.figure(figsize=(12, 6))
    if 'mom_percentage_change' in econ_df.columns:
        plt.plot(econ_df.index, econ_df['mom_percentage_change'], label='Month-over-Month Percentage Change', color='blue')
    if 'yoy_percentage_change' in econ_df.columns:
        plt.plot(econ_df.index, econ_df['yoy_percentage_change'], label='Year-over-Year Percentage Change', color='red')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'output/{title.replace(" ", "_").replace("/", "_")}.png')
    plt.show()

def plot_stock_prices(stock_data):
    for ticker, df in stock_data.items():
        plt.figure(figsize=(12, 6))
        if 'Adj Close' in df.columns:
            plt.plot(df.index, df['Adj Close'], label=f'{ticker} Adjusted Close Price', color='green')
        else:
            print(f"Warning: 'Adj Close' column not found for {ticker}. Available columns: {df.columns.tolist()}")
        
        plt.title(f'{ticker} Adjusted Close Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'output/{ticker}_adjusted_close_price.png')
        plt.show()
