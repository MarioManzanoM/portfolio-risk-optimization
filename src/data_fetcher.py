# Obtaining historical stock data using yfinance library
import yfinance as yf
import pandas as pd
import requests
from src.utils import Date


# Fetch historical stock data for a given ticker, date range, and frequency
def fetch_stock_data(ticker: str, start: Date, end: Date, interval: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, start=start.value, end=(end+1).value, interval=interval)
        df = df.dropna()
        
        if df.empty:
            print(f"Aviso: No se encontraron datos válidos para {ticker}")
            return None
            
        return df
        
    except Exception as e:
        print(f"Error descargando datos para {ticker}: {e}")
        return None
    

# Fetch ticker from company name using yfinance library
def get_ticker_from_name(company_name: str) -> str:
    url = "https://query2.finance.yahoo.com/v1/finance/search"
    
    params = {
        "q": company_name,
        "quotesCount": 1, # First result
        "newsCount": 0    # Do not want extra info
    }
    
    # Have to ask as a navigator and not as an script
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status() 
        
       
        data = response.json()
        
        if 'quotes' in data and len(data['quotes']) > 0:
            ticker = data['quotes'][0]['symbol']
            return ticker
        else:
            print(f"Warning: no ticker found for '{company_name}'.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Connection error while searching for'{company_name}': {e}")
        return None
    


# Fetch first available date for a given ticker using yfinance library
def get_first_date_from_df(df: pd.DataFrame) -> str:
    if df is not None and not df.empty:
        return df.index[0].strftime("%Y-%m-%d")
    return None
    
# Fetch last available date for a given ticker using yfinance library
def get_last_date_from_df(df: pd.DataFrame) -> str:
    if df is not None and not df.empty:
        return df.index[-1].strftime("%Y-%m-%d")
    return None