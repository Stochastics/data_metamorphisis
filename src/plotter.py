import matplotlib.pyplot as plt
import os

import matplotlib.pyplot as plt
import polars as pl

def plot_econ_data(econ_df, title='Economic Data', y_label='Value'):
    """
    Plot economic data using Polars DataFrame and Matplotlib.

    Args:
        econ_df (pl.DataFrame): The Polars DataFrame containing the economic data.
        title (str): The title of the plot.
        y_label (str): The label for the Y-axis.
    """
    # Convert Polars DataFrame to a format suitable for Matplotlib (using lists)
    dates = econ_df['date'].to_list()
    values = econ_df['value'].to_list()

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(dates, values, label='Economic Data', marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(y_label)
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_stock_prices(stock_df, value_column, title='Stock Prices'):
    """
    Plot stock prices using Polars DataFrame and Matplotlib.

    Args:
        stock_df (pl.DataFrame): The Polars DataFrame containing the stock data.
        value_column (str): The column name for the values to plot (e.g., 'Adj Close').
        title (str): The title of the plot.
    """
    # Convert Polars DataFrame to a format suitable for Matplotlib (using lists)
    dates = stock_df['Date'].to_list()
    values = stock_df[value_column].to_list()

    # Plot the data
    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, label=value_column, marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Adjusted Close Price')
    plt.grid(True)
    plt.legend()
    plt.show()
