import matplotlib.pyplot as plt

def plot_cpi_changes(cpi_df):
    plt.figure(figsize=(12, 6))
    if 'monthly_inflation_rate' in cpi_df.columns:
        plt.plot(cpi_df.index, cpi_df['monthly_inflation_rate'], label='Monthly Inflation Rate', color='blue')
    if 'yoy_inflation_rate' in cpi_df.columns:
        plt.plot(cpi_df.index, cpi_df['yoy_inflation_rate'], label='YOY Inflation Rate', color='red')
    plt.title('CPI Inflation Rate Over Time')
    plt.xlabel('Date')
    plt.ylabel('Inflation Rate (%)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('output/cpi_inflation_rate.png')
    plt.show()

def plot_stock_prices(stock_data):
    for ticker, df in stock_data.items():
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['Adj Close'], label=f'{ticker} Adjusted Close Price', color='green')
        plt.title(f'{ticker} Adjusted Close Price Over Time')
        plt.xlabel('Date')
        plt.ylabel('Adjusted Close Price')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'output/{ticker}_adjusted_close_price.png')
        plt.show()
