import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pytz import timezone
import yfinance as yf

from base_miner.get_data import prep_data, scale_data, round_down_time

from tensorflow.keras.models import load_model

def predict(timestamp, scaler, model):
    # calling this to get the last timestamp present for which a next close hasn't been decided yet
    data = prep_data(drop_na=False)
    data['Datetime'] = pd.to_datetime(data['Datetime'])

    pred_time = round_down_time(datetime.fromisoformat(timestamp))

    matching_row = data[data['Datetime'] == pred_time]

    print(pred_time, matching_row)

    # Check if matching_row is empty
    if matching_row.empty:
        print("No matching row found for the given timestamp.")
        return 0.0

    # data.to_csv('tester.csv')
    input = matching_row[['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'CCI', 'Momentum']]

    input = np.array(input, dtype=np.float32).reshape(1,-1)
    input = np.reshape(input, (1,1, input.shape[1]))
    print(input)

    prediction = model.predict(input)
    prediction = scaler.inverse_transform(prediction)

    return prediction

'''if(__name__=='__main__'):
    data = prep_data()
    scaler, X, y = scale_data(data)
    model = load_model('mining_models/base_lstm.h5')
    ny_timezone = timezone('America/New_York')
    current_time_ny = datetime.now(ny_timezone)
    timestamp = current_time_ny.isoformat()


    #mse = create_and_save_base_model(scaler, X, y)
    prediction = predict(timestamp, scaler, model)
    print(prediction)'''
    


