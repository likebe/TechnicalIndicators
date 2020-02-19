import pandas_datareader as web
import pandas as pd
import numpy as np


symbols = ['QQQ']

start = 'JAN-01-2010'
end = 'Jan-07-2020'
api_key = 'sA3Rkz75zLLgZDYeX35s'
prices = pd.DataFrame(index=pd.date_range(start, end))

for symbol in symbols:
	portfolio = web.DataReader(name=symbol, data_source='yahoo', start=start, end=end,
							   api_key=api_key)
portfolio = portfolio.dropna()
print(portfolio)
prices = portfolio[['Open', 'High', 'Low', 'Close', 'Volume']]
print(prices)


# Simple Moving Average
def SMA (ticker_df, periods = 20):
	ticker_df['SMA'] = ticker_df['Close'].rolling(window=periods).mean()
	return ticker_df


# Exponential Moving Average
def EMA(ticker_df, periods = 20):
	ticker_df['EMA'] = pd.ewma(ticker_df['Close'], span=periods)
	return ticker_df


# MACD (Moving Average Convergence Divergence)
def MACD(ticker_df):
	ticker_df['MACD'] = (pd.ewma(ticker_df['Close'], span=12) - pd.ewma(ticker_df['Close'], span=26))
	return ticker_df


# stochastic oscillator
def STOK(close, low, high, n):
	STOK = ((close - pd.rolling_min(low, n)) / (pd.rolling_max(high, n) - pd.rolling_min(low, n))) * 100
	return STOK


def STOD(close, low, high, n):
	STOK = ((close - pd.rolling_min(low, n)) / (pd.rolling_max(high, n) - pd.rolling_min(low, n))) * 100
	STOD = pd.rolling_mean(STOK, 3)
	return STOD


def stochastic_oscillator(ticker_df):
	ticker_df['%K'] = STOK(ticker_df['Close'], ticker_df['Low'], ticker_df['High'], 14)
	ticker_df['%D'] = STOK(ticker_df['Close'], ticker_df['Low'], ticker_df['High'], 14)
	return ticker_df


# accumulation distribution
def accumulation_distribution(ticker_df):
	multiplier = ((ticker_df['Close']-ticker_df['Low']) - (ticker_df['High']-ticker_df['Close'])) / (ticker_df['High'] - ticker_df['Low'])
	CMFV = multiplier*ticker_df['Volume']
	ticker_df['A/D'] = CMFV
	ticker_df['A/D'] = ticker_df['A/D'].cumsum(axis=1)
	return ticker_df


# Bollinger Band
def bbands(ticker_df, window_size = 20, num_of_std = 2):
	ticker_df['MidBand'] = SMA(ticker_df, periods=window_size)
	rolling_std = ticker_df['Close'].rolling(window=window_size).std()
	ticker_df['UpperBand'] = ticker_df['MidBand'] + (rolling_std * num_of_std)
	ticker_df['LowerBand'] = ticker_df['MidBand'] - (rolling_std * num_of_std)
	return ticker_df


# on-balance volume
def obv(ticker_df):
	ticker_df['prev_close'] = ticker_df['Close'].shift(-1)
	ticker_df['obv'] = ticker_df['Volume'] if (ticker_df['prev_close'] < ticker_df['Close']) elif (ticker_df['prev_close'] == ticker_df['Close']) 0 else (-ticker_df['Volume'])