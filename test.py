import yfinance as yf
from datetime import datetime, timedelta
from pytz import timezone


# Define the ticker symbol for the S&P 500
ticker_symbol = '^GSPC'

# Create a ticker object
ticker = yf.Ticker(ticker_symbol)

current_time = datetime.now()
print(current_time)


# current_time_adjusted = current_time - timedelta(minutes=10)

# data = ticker.history(start=current_time_adjusted, end=current_time, interval='5m')

# print(len(data))
# print(data)

# most_recent_close_price = data['Close'].iloc[-1]
# print("Most Recent Close Price:", most_recent_close_price)



# Round down the time to the nearest interval
rounded_dt = current_time - timedelta(minutes=current_time.minute % 5,
                                seconds=current_time.second,
                                microseconds=current_time.microsecond) + timedelta(minutes=5)

print(rounded_dt)