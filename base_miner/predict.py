import numpy as np
from get_data import prep_data, scale_data, round_down_time
from model import create_and_save_base_model
from tensorflow.keras.models import load_model

def predict(scaler, model):
    # calling this to get the last timestamp present for which a next close hasn't been decided yet
    data = prep_data(drop_na=False)
    data.to_csv('tester.csv')
    input = data.iloc[-1][['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'CCI', 'Momentum']]
    input = np.array(input).reshape(1,-1)
    input = np.reshape(input, (1,1, input.shape[1]))
    print(input)

    prediction = model.predict(input)
    prediction = scaler.inverse_transform(prediction)

    return prediction

if(__name__=='__main__'):
    data = prep_data()
    scaler, X, y = scale_data(data)
    #mse = create_and_save_base_model(scaler, X, y)
    prediction = predict(scaler)
    print(prediction)
    


