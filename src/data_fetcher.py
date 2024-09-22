import requests
import polars as pl
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('FRED_API_KEY')

def fetch_fred_data(series_id, start_date='2000-01-01', end_date='2024-12-31', frequency='m'):
    url = 'https://api.stlouisfed.org/fred/series/observations'
    params = {
        'series_id': series_id,
        'api_key': API_KEY,
        'file_type': 'json',
        'observation_start': start_date,
        'observation_end': end_date,
        'frequency': frequency
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'observations' in data:
            df = pl.DataFrame(data['observations'])
            if not df.is_empty():
                df = df.with_columns([
                    pl.col('date').str.strptime(pl.Date, '%Y-%m-%d').alias('date'),
                    pl.col('value').cast(pl.Float64, strict=False)
                ])
                df = df.sort('date')
                return df
    return pl.DataFrame()
