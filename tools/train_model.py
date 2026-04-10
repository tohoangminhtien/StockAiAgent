import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from vnstock import Vnstock
from datetime import date
from dateutil.relativedelta import relativedelta


def predict_stock(symbol: str):
    # Get data
    stock = Vnstock().stock(symbol=symbol, source='TCBS')
    end = date.today()
    start = end - relativedelta(years=3)
    df = stock.quote.history(start=str(start), end=str(end))
    series = df['open'].tolist()
    data = np.array(series).reshape(-1, 1)

    # Normalize
    scaler = MinMaxScaler()
    data_scaled = scaler.fit_transform(data)

    # Split X, y
    window_size = 30
    X, y = create_sequences(data_scaled, window_size)

    # Split train/test
    train_size = int(len(X) * 0.8)
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Model
    model = tf.keras.Sequential([
        tf.keras.layers.Input((window_size, 1)),
        tf.keras.layers.LSTM(64, return_sequences=True),
        tf.keras.layers.LSTM(64, return_sequences=True),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    # Compile
    model.compile(optimizer='adam', loss='mse')

    # Train
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=32,
        validation_split=0.1,
        verbose=1
    )

    # Predict
    y_pred = model.predict(X_test)

    # Valid set
    import math
    from sklearn.metrics import mean_squared_error

    y_pred = scaler.inverse_transform(y_pred[:, -1, :])
    y_test = scaler.inverse_transform(y_test[:, -1, :])

    # Tính MSE
    mse = mean_squared_error(y_pred[:, 0], y_test[:, 0])
    print("Mean Squared Error:", mse)

    rmse = math.sqrt(mse)
    print("RMSE: ", rmse)
    plt.figure(figsize=(12, 6))

    # Tạo trục thời gian đầy đủ 31 ngày (0-30)
    time_points = np.arange(31)

    # Nối dữ liệu X và y
    x_new = np.expand_dims(data_scaled[-30:], axis=0)
    y_new = model.predict(x_new)

    # Inverse transform
    x_new = scaler.inverse_transform(x_new[:, :, 0])
    y_new = scaler.inverse_transform(y_new[:, :, 0])

    # Shape
    print('X shape', x_new.shape)
    print('y shape', y_new.shape)
    full_data = np.append(x_new, y_new[:, -1])

    # Vẽ đường kẻ cho toàn bộ dữ liệu
    plt.plot(time_points, full_data,
             color='#1f77b4',
             label='Data',
             linewidth=2)

    # Thêm dấu sao tại điểm dự đoán
    plt.scatter(30, y_new[:, -1],
                color='red',
                marker='*',
                s=200,
                label='Prediction',
                zorder=5)

    plt.title('30-Day History and Next Day Prediction', fontsize=14, pad=15)
    plt.xlabel('Days', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.grid(True)
    plt.legend(fontsize=10)
    plt.margins(x=0.02)
    plt.tight_layout()
    plt.savefig(f"chart/{symbol}-{str(end)}.png", dpi=300)

    return f"{symbol} stock opening price tomorrow is {y_new[0, -1]} (RMSE = {rmse})"


def create_sequences(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i+window_size])
        y.append(data[i+1:i+window_size+1])
    return np.array(X), np.array(y)
