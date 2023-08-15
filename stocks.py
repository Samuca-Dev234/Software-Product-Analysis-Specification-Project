import yfinance as yf
import pandas as pd

symbols = ['ROMI3.SA', 'RAPT4.SA', 'ITUB4.SA', 'GGBR4.SA', 'WEGE3.SA', '^BVSP']

start_date = '2020-01-01'
end_date = '2023-08-11'

data = yf.download(symbols, start=start_date, end=end_date)['Adj Close']


column_mapping = {
    'ROMI3.SA': 'romi',
    'RAPT4.SA': 'rapt',
    'ITUB4.SA': 'itub',
    'GGBR4.SA': 'ggbr',
    'WEGE3.SA': 'Wweg',
    '^BVSP': 'ibov'
}

data.rename(columns=column_mapping, inplace=True)

data['Date'] = pd.to_datetime()

data.set_index('Date', inplace=True)

data.to_csv('stock_prices.csv')
