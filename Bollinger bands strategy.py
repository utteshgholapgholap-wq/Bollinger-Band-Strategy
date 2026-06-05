import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Initialize asset dataframe
data = {"Close": [100, 101, 99, 98, 95, 94, 96, 98, 102, 105, 107, 104, 101, 100]}
df = pd.DataFrame(data)

# 2. Parameters
lookback = 5
std_multiplier = 2

# 3. Calculate Bands
df["Middle_Band"] = df["Close"].rolling(window=lookback).mean()
df["Std_Dev"] = df["Close"].rolling(window=lookback).std()
df["Upper_Band"] = df["Middle_Band"] + (std_multiplier * df["Std_Dev"])
df["Lower_Band"] = df["Middle_Band"] - (std_multiplier * df["Std_Dev"])

# 4. Vectorized Signal Mapping
conditions = [
    df["Close"] < df["Lower_Band"],  # Oversold condition
    df["Close"] > df["Upper_Band"],  # Overbought condition
]
choices = ["BUY", "SELL"]
df["Signal"] = np.select(conditions, choices, default="HOLD")

# Drop initialization rows for clean printing, but we keep a copy for continuous plotting
df_clean = df.dropna().copy()
print(df_clean[["Close", "Upper_Band", "Lower_Band", "Signal"]])

# ==========================================
# 5. VISUALIZATION FEATURES
# ==========================================
plt.figure(figsize=(12, 6))
plt.style.use("seaborn-v0_8-darkgrid")  # Clean modern grid style

# Plot Close Price and Bollinger Bands
plt.plot(df.index, df["Close"], label="Close Price", color="blue", linewidth=2)
plt.plot(
    df.index,
    df["Upper_Band"],
    label="Upper Band",
    color="red",
    linestyle="--",
    alpha=0.7,
)
plt.plot(
    df.index,
    df["Middle_Band"],
    label="Middle Band (SMA)",
    color="gray",
    linestyle=":",
    alpha=0.5,
)
plt.plot(
    df.index,
    df["Lower_Band"],
    label="Lower Band",
    color="green",
    linestyle="--",
    alpha=0.7,
)

# Shading the area between the bands
plt.fill_between(
    df.index,
    df["Upper_Band"],
    df["Lower_Band"],
    color="grey",
    alpha=0.1,
    label="Volatility Band",
)

# Plotting BUY Signals (Green Up Triangles)
buy_signals = df[df["Signal"] == "BUY"]
plt.scatter(
    buy_signals.index,
    buy_signals["Close"],
    color="green",
    marker="^",
    s=150,
    label="BUY Signal",
    zorder=5,
)

# Plotting SELL Signals (Red Down Triangles)
sell_signals = df[df["Signal"] == "SELL"]
plt.scatter(
    sell_signals.index,
    sell_signals["Close"],
    color="red",
    marker="v",
    s=150,
    label="SELL Signal",
    zorder=5,
)

# Chart Titles and Labels
plt.title(
    f"Bollinger Bands Strategy (Lookback: {lookback}, Std Dev: {std_multiplier})",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Timeline / Index", fontsize=12)
plt.ylabel("Price", fontsize=12)
plt.xticks(df.index)  # Ensure all data points align on x-axis

# Legend configuration
plt.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")

# Show the plot
plt.tight_layout()
plt.show()