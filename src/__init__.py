# src/__init__.py

from .data_fetcher import fetch_data
from .data_processor import process_data
from .plotter import plot_data

__all__ = ['fetch_data', 'process_data', 'plot_data']