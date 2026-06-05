import numpy as np
import pandas as pd

# 1. Create simple mock data
data = {
    "Close": [
        100,
        101,
        99,
        98,
        95,
        94,
        96,
        98,
        102,
        105,
        107,
        104,
        101,
        100,
    ]
}
df = pd.DataFrame(data)

# 2. Calculate Bollinger Bands (using a small 5-period window for this example)
lookback = 5
df["Middle_Band"] = df["Close"].rolling(window=lookback).mean()
df["Std_Dev"] = df["Close"].rolling(window=lookback).std()

df["Upper_Band"] = df["Middle_Band"] + (2 * df["Std_Dev"])
df["Lower_Band"] = df["Middle_Band"] - (2 * df["Std_Dev"])

# 3. Generate Signals
# np.select applies conditions in order: if True -> assigns the corresponding label
conditions = [
    df["Close"] < df["Lower_Band"],  # Condition 1: Price punctures bottom
    df["Close"] > df["Upper_Band"],  # Condition 2: Price punctures top
]
choices = ["BUY", "SELL"]

df["Signal"] = np.select(conditions, choices, default="HOLD")

# Drop rows that don't have enough data to calculate the moving average
df.dropna(inplace=True)
print(df[["Close", "Upper_Band", "Lower_Band", "Signal"]])