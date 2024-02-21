import numpy as np
from get_data import prep_data, round_down_time
from model import create_and_save_base_model
from tensorflow.keras.models import load_model

def predict(scaler):
    scaler = create_and_save_base_model(data)
    model = load_model('mining_models/base_lstm.h5')
    pred = predict(scaler)
    data = prep_data(drop_na=False)
    data.to_csv('tester.csv')
    input = data.iloc[-1][['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'CCI', 'Momentum']]
    input = np.array(input).reshape(1,-1)
    input = np.reshape(input, (1,1, input.shape[1]))
    print(input)
    prediction = model.predict(input)

    prediction = scaler.inverse_transform(prediction)

    return prediction
