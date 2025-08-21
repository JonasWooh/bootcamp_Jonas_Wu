from __future__ import annotations
import os
import pathlib
import datetime as dt
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv

RAW = pathlib.Path('data/raw')
RAW.mkdir(parents=True, exist_ok=True)
load_dotenv()

def ts() -> str:
    return dt.datetime.now().strftime('%Y%m%d-%H%M%S')

def save_csv(df: pd.DataFrame, prefix: str, **meta) -> pathlib.Path:
    mid = '_'.join([f"{k}-{v}" for k, v in meta.items()])
    path = RAW / f"{prefix}_{mid}_{ts()}.csv"
    df.to_csv(path, index=False)
    print("Saved", path)
    return path

def validate(df: pd.DataFrame, required):
    missing = [c for c in required if c not in df.columns]
    return {'missing': missing, 'shape': df.shape, 'na_total': int(df.isna().sum().sum())}

def acquire_api(symbol: str = 'AAPL') -> pd.DataFrame:
    use_alpha = bool(os.getenv('ALPHAVANTAGE_API_KEY'))
    if use_alpha:
        url = 'https://www.alphavantage.co/query'
        params = {'function':'TIME_SERIES_DAILY','symbol':symbol,'outputsize':'full','apikey':os.getenv('ALPHAVANTAGE_API_KEY')}
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        js = r.json()
        key = [k for k in js if 'Time Series' in k][0]
        df_api = pd.DataFrame(js[key]).T
        df_api.columns = [c.split('. ')[1] for c in df_api.columns]
        df_api = df_api.reset_index().rename(columns={'index':'date'})
        df_api['date'] = pd.to_datetime(df_api['date'])
        for col in ['open','high','low','close','volume']:
            df_api[col] = pd.to_numeric(df_api[col], errors='coerce')
    else:
        import yfinance as yf
        df_api = yf.download(symbol, period='3mo', interval='1d').reset_index()
        df_api = df_api.rename(columns={'Date':'date','Open':'open','High':'high','Low':'low','Close':'close','Volume':'volume'})
    required_cols = ['date','open','high','low','close','volume']
    v = validate(df_api, required_cols)
    print("API Validation Results:", v)
    return df_api

def acquire_scrape(url: str = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies') -> pd.DataFrame:
    headers = {'User-Agent':'AFE-Project/1.0'}
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = [[c.get_text(strip=True) for c in tr.find_all(['th','td'])] for tr in soup.find_all('tr')]
        header, *data = [r for r in rows if r]
        df_scrape = pd.DataFrame(data, columns=header)
    except Exception as e:
        print('Scrape failed, using inline demo table:', e)
        html = '<table><tr><th>Ticker</th><th>Price</th></tr><tr><td>AAA</td><td>101.2</td></tr></table>'
        soup = BeautifulSoup(html, 'html.parser')
        rows = [[c.get_text(strip=True) for c in tr.find_all(['th','td'])] for tr in soup.find_all('tr')]
        header, *data = [r for r in rows if r]
        df_scrape = pd.DataFrame(data, columns=header)
    if 'Price' in df_scrape.columns:
        df_scrape['Price'] = pd.to_numeric(df_scrape['Price'], errors='coerce')
    required_cols = ['Symbol','Security']
    v = {'missing':[c for c in required_cols if c not in df_scrape.columns], 'shape': df_scrape.shape, 'na_total': int(df_scrape.isna().sum().sum())}
    print("Scrape Validation Results:", v)
    return df_scrape

def main():
    df_api = acquire_api('AAPL')
    _ = save_csv(df_api.sort_values('date'), prefix='api', source='alpha' if bool(os.getenv('ALPHAVANTAGE_API_KEY')) else 'yfinance', symbol='AAPL')

    df_scrape = acquire_scrape()
    _ = save_csv(df_scrape, prefix='scrape', site='wikipedia', table='SP500-List')

if __name__ == "__main__":
    main()
