from get_data import prep_data

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def create_and_save_base_model(data):
    model_name = "mining_models/base_lstm"
    X = data[['Open', 'High', 'Low', 'Volume', 'SMA_50', 'SMA_200', 'RSI', 'CCI', 'Momentum']].values

    # Prepare target variable
    y = data[['NextClose']].values

    # Scale features
    scaler = MinMaxScaler(feature_range=(0, 1))
    X_scaled = scaler.fit_transform(X)
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).reshape(-1)

    # Reshape input for LSTM
    X_scaled = X_scaled.reshape((X_scaled.shape[0], 1, X_scaled.shape[1]))

    # Split data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

    # LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(X_scaled.shape[1], X_scaled.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, epochs=100, batch_size=32)
    model.save(f'{model_name}.h5')
    # Predict
    predicted_prices = model.predict(X_test)

    # Rescale back to original range
    predicted_prices = scaler.inverse_transform(predicted_prices)
    y_test_rescaled = scaler.inverse_transform(y_test.reshape(-1, 1))

    # Evaluate
    mse = mean_squared_error(y_test_rescaled, predicted_prices)
    print(f'Mean Squared Error: {mse}')

    return scaler