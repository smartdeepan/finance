import re
import time
from dataclasses import dataclass
from io import StringIO

import pandas as pd
import requests

from scripts.index_funds_fetcher import get_invested_indices_urls

# Define a custom User-Agent to avoid being blocked by servers.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

@dataclass
class IndexOverlap:
    """
    A dataclass to store the portfolio overlap analysis.

    Attributes:
        overlap (dict): A dictionary where keys are stock symbols and values are lists of indices
                       that the stock is present in.
    """
    overlap: dict


def extract_index_name(url: str) -> str:
    """
    Extracts the index name (e.g., 'nifty50') from a Nifty Indices URL.

    Handles both the older URL format and the newer format from niftyindices.com.

    Args:
        url (str): The URL of the Nifty Indices CSV file.

    Returns:
        str: The extracted index name or the original URL if extraction fails.
    """
    match = re.search(r"ind_nifty(\d+)list\.csv", url)  # Regular expression search (old format)
    if match:
        return ("nifty" + match.group(1)).replace("ind_", "").replace("list", "")
    else:
        prefix = "https://www.niftyindices.com/IndexConstituent/" # New format
        if url.startswith(prefix):
            index_name = url[len(prefix):]
            return index_name[:-4].replace("ind_", "").replace("list", "") # Remove prefix and .csv
        else:
            return url  # Return the original URL if no match is found


def analyze_portfolio_overlap(urls: list) -> IndexOverlap:
    """
    Analyzes portfolio overlap across a list of Nifty Indices URLs.

    Args:
        urls (list): A list of URLs pointing to Nifty Indices CSV files.

    Returns:
        IndexOverlap: An IndexOverlap object containing the overlap analysis, even if errors occurred.
                      The overlap dictionary might be empty if all URLs had errors.
    """
    index_To_stocks = dict()  # Dictionary to store index names as keys and lists of stocks as values.
    stock_to_Indices = dict() # Dictionary to store stock symbols as keys and lists of indices as values.
    overlap = dict()
    index_overlap: IndexOverlap = IndexOverlap(overlap=overlap) # Initialize the dataclass

    for url in urls:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            df = pd.read_csv(StringIO(response.text)) # Use StringIO to parse the CSV from the response text

            stock_symbols = df["Symbol"].tolist()
            index_To_stocks[extract_index_name(url)] = stock_symbols

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            continue # Continue to the next URL even if there's an error
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV from {url}: {e}")
            continue # Continue to the next URL even if there's an error
        except Exception as e:
            print(f"An unexpected error occurred while processing {url}: {e}")
            continue # Continue to the next URL even if there's an error
        finally:
            time.sleep(1)  # Introduce a small delay to be polite to the server

    for index, stocks in index_To_stocks.items():
        for stock in stocks:
            if stock not in stock_to_Indices: # Simplified check
                stock_to_Indices[stock] = [] # Initialize the list if the stock is not present
            stock_to_Indices[stock].append(index)

    index_overlap.overlap = stock_to_Indices # Set the dataclass overlap attribute
    return index_overlap


if __name__ == "__main__":
    portfolio_urls = get_invested_indices_urls()

    overlap_analysis = analyze_portfolio_overlap(portfolio_urls.values())

    if overlap_analysis and overlap_analysis.overlap:  # Check if the object exists AND the overlap is not empty
        print("Portfolio Overlap Analysis:")
        sorted_by_count = sorted(overlap_analysis.overlap.items(), key=lambda item: len(item[1]), reverse=True)
        for stock, indices in sorted_by_count:
            if len(indices) > 1:
                print(f"{stock}: Present in {len(indices)} portfolios within {indices}")
    else:
        print("No overlapping stocks found or an error occurred during analysis.")