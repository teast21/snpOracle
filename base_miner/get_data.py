from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import yfinance as yf
import ta

def prep_data(drop_na=True):
    # Fetch S&P 500 data
    data = yf.download('^GSPC', period='60d', interval='5m')

    data.to_csv('mining_models/tester.csv')

    # Calculate technical indicators
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()
    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    data['CCI'] = ta.trend.CCIIndicator(data['High'], data['Low'], data['Close']).cci()
    data['Momentum'] = ta.momentum.ROCIndicator(data['Close']).roc()
    data['NextClose'] = data['Close'].shift(-1)

    # Drop NaN values
    if(drop_na):
        data.dropna(inplace=True)

    return data

def round_down_time(unix_timestamp, interval_minutes=5):
    # Convert the Unix timestamp to a datetime object
    dt = datetime.utcfromtimestamp(unix_timestamp)

    # Round down the time to the nearest interval
    rounded_dt = dt - timedelta(minutes=dt.minute % interval_minutes,
                                seconds=dt.second,
                                microseconds=dt.microsecond)

    return rounded_dt

def scale_data(data):
    X = data[['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'CCI', 'Momentum']].values

    # Prepare target variable
    y = data[['NextClose']].values

    # Scale features
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled = scaler.fit_transform(X)
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).reshape(-1)

    return scaler, X_scaled, y_scaled


