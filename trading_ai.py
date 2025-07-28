# Install necessary libraries if you haven't already:
# It's recommended to use a virtual environment.
# python -m venv venv
# .\venv\Scripts\activate  (Windows) or source venv/bin/activate (macOS/Linux)
#
# Try installing specific TensorFlow versions if you encounter issues:
# pip install tensorflow==2.10.0 # A common stable version
# Or for newer Python versions, you might need a more recent TF:
# pip install tensorflow==2.13.0
#
# Then install the other libraries:
# pip install yfinance pandas numpy scikit-learn matplotlib ta

import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
import ta # Technical Analysis library

# --- Configuration ---
STOCK_TICKER = 'AAPL' # Apple Inc.
START_DATE = '2018-01-01'
END_DATE = '2023-01-01' # Using historical data up to this point for training
PREDICTION_DAYS = 60 # Number of past days to consider for each prediction
EPOCHS = 25 # Number of training epochs
BATCH_SIZE = 32 # Batch size for training

# --- 1. Fetch Historical Data ---
print(f"Fetching historical data for {STOCK_TICKER} from {START_DATE} to {END_DATE}...")
try:
    df = yf.download(STOCK_TICKER, start=START_DATE, end=END_DATE)
    if df.empty:
        print(f"No data fetched for {STOCK_TICKER}. Please check the ticker symbol or date range.")
        exit()
    print("Data fetched successfully!")
except Exception as e:
    print(f"Error fetching data: {e}")
    exit()

# Use 'Close' price for prediction
data = df[['Close']].copy()

# --- 2. Feature Engineering ---
print("Calculating technical indicators...")
# Simple Moving Averages
data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
data['SMA_50'] = ta.trend.sma_indicator(data['Close'], window=50)

# Relative Strength Index (RSI)
data['RSI'] = ta.momentum.rsi(data['Close'], window=14)

# Drop rows with NaN values resulting from indicator calculations
data.dropna(inplace=True)
print(f"Data after feature engineering and NaN removal. Shape: {data.shape}")

# --- 3. Data Preprocessing ---
print("Preprocessing data for LSTM...")

# Scale the features
# We scale all features, including the target 'Close'
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data)

# Create sequences for LSTM
# X will be the input features (scaled prices and indicators for PREDICTION_DAYS)
# Y will be the target (the next day's 'Close' price, scaled)
X, y = [], []
for i in range(PREDICTION_DAYS, len(scaled_data)):
    X.append(scaled_data[i-PREDICTION_DAYS:i]) # Sequence of PREDICTION_DAYS
    # The target is the 'Close' price of the current day (index 0 in 'data' columns after dropping NaNs)
    y.append(scaled_data[i, 0]) # Assuming 'Close' is the first column after scaling

X, y = np.array(X), np.array(y)

# Reshape X for LSTM input: (samples, time_steps, features)
# The number of features is the number of columns in our 'data' DataFrame
X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2])) # X.shape[2] is num_features

print(f"X shape: {X.shape} (samples, time_steps, features)")
print(f"y shape: {y.shape} (samples, target_value)")

# Split data into training and testing sets
# It's crucial to maintain time series order for validation
train_size = int(len(X) * 0.8) # 80% for training
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

print(f"Training set size: {len(X_train)} samples")
print(f"Test set size: {len(X_test)} samples")

# --- 4. Build LSTM Model ---
print("Building LSTM model...")
model = Sequential()
# First LSTM layer with return_sequences=True to pass output to next LSTM layer
model.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2)) # Dropout for regularization to prevent overfitting

# Second LSTM layer
model.add(LSTM(units=50, return_sequences=False)) # return_sequences=False for the last LSTM layer before Dense
model.add(Dropout(0.2))

# Output layer: Dense layer for a single price prediction
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# --- 5. Train Model ---
print("Training the model...")
history = model.fit(X_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.1, verbose=1)
print("Model training complete.")

# --- 6. Make Predictions ---
print("Making predictions on test data...")
predictions = model.predict(X_test)

# Inverse transform the predictions and actual values to original scale
# We need to create a dummy array with the same number of features as scaled_data
# so that the inverse_transform can correctly convert back only the 'Close' price.
# The 'Close' price is the first column (index 0).
dummy_predictions = np.zeros(shape=(len(predictions), scaled_data.shape[1]))
dummy_predictions[:,0] = predictions[:,0]
predictions = scaler.inverse_transform(dummy_predictions)[:,0]

dummy_y_test = np.zeros(shape=(len(y_test), scaled_data.shape[1]))
dummy_y_test[:,0] = y_test
y_test_unscaled = scaler.inverse_transform(dummy_y_test)[:,0]

# --- 7. Visualize Results ---
print("Generating plot of predictions vs actual prices...")

# Create a DataFrame for plotting, aligning predictions with original dates
# Adjust the index of y_test_unscaled to match the original data's dates
# The test data starts from `df.index[len(df) - len(X_test)]`
# This can be tricky due to `dropna` and `PREDICTION_DAYS` offsetting.
# A simpler approach for visualization is to reconstruct the full 'Close' series and overlay.

# To get the full unscaled data (original 'Close' prices) for plotting
# We use the original 'data' DataFrame and slice it correctly for the test period.
test_dates = df.index[len(df) - len(y_test_unscaled):].values
actual_prices = df['Close'].iloc[len(df) - len(y_test_unscaled):].values

plt.figure(figsize=(14, 7))
plt.plot(test_dates, actual_prices, color='blue', label=f'Actual {STOCK_TICKER} Price')
plt.plot(test_dates, predictions, color='red', label=f'Predicted {STOCK_TICKER} Price')
plt.title(f'{STOCK_TICKER} Price Prediction')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.show()

print("\n--- Next Steps & Considerations for Real-Time ---")
print("1. Real-time Data: To predict in real-time, you'd integrate with a live data API (e.g., Alpaca, OANDA).")
print("   You would continuously fetch new data, update your feature set, and pass a 'PREDICTION_DAYS' sequence to the model.")
print("2. Deployment: Deploying this model for real-time inference would involve a server (e.g., Flask, FastAPI) that receives data, makes predictions, and potentially sends signals.")
print("3. More Features: Explore more complex technical indicators, volume analysis, and sentiment analysis.")
print("4. Hyperparameter Tuning: Optimize LSTM units, dropout rates, learning rates, etc.")
print("5. Robustness: Implement error handling, logging, and monitoring for a production-ready system.")
print("6. Backtesting: Rigorously backtest any trading strategy based on these predictions on unseen historical data, accounting for transaction costs and slippage.")
print("7. Risk Management: Essential for any trading system. Never trade with real money based solely on AI predictions without understanding and managing the risks.")
