import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 1. Load and Prepare Tesla Dataset
df = pd.read_csv('Tesla.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df = df.sort_values('Date').reset_index(drop=True)

# 2. Parameters (Adjusted lookback to industry-standard 20)
lookback = 20
std_multiplier = 2

# 3. Calculate Bollinger Bands
df["Middle_Band"] = df["Close"].rolling(window=lookback).mean()
df["Std_Dev"] = df["Close"].rolling(window=lookback).std()
df["Upper_Band"] = df["Middle_Band"] + (std_multiplier * df["Std_Dev"])
df["Lower_Band"] = df["Middle_Band"] - (std_multiplier * df["Std_Dev"])

# 4. Vectorized Signal Mapping
conditions = [
    df["Close"] < df["Lower_Band"],  # Oversold condition (BUY)
    df["Close"] > df["Upper_Band"]   # Overbought condition (SELL)
]
choices = ["BUY", "SELL"]
df["Signal"] = np.select(conditions, choices, default="HOLD")

# ==========================================
# 5. BACKTESTING LOGIC
# ==========================================
# Track positions: 1 for Long (after BUY), 0 for Flat (after SELL)
df['Position'] = np.nan
df.loc[df['Signal'] == 'BUY', 'Position'] = 1
df.loc[df['Signal'] == 'SELL', 'Position'] = 0
df['Position'] = df['Position'].ffill().fillna(0)

# Calculate daily strategy returns (shifting position by 1 day to prevent look-ahead bias)
df['Daily_Return'] = df['Close'].pct_change()
df['Strategy_Return'] = df['Position'].shift(1) * df['Daily_Return']

# Compute cumulative growth
df['Cum_Buy_Hold'] = (1 + df['Daily_Return'].fillna(0)).cumprod() - 1
df['Cum_Strategy'] = (1 + df['Strategy_Return'].fillna(0)).cumprod() - 1

# Save backtest results to a fresh CSV file
df.to_csv('Tesla_Bollinger_Backtest.csv', index=False)
print("Backtest data saved to 'Tesla_Bollinger_Backtest.csv'")

# ==========================================
# 6. VISUALIZATION FEATURES (CORRECTED)
# ==========================================
# Setup a 2-panel figure to track prices and backtest performance side-by-side
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
plt.style.use("seaborn-v0_8-darkgrid")

# Top Panel: Close Price & Bollinger Bands
ax1.plot(df['Date'], df["Close"], label="Close Price", color="blue", linewidth=1.5)
ax1.plot(df['Date'], df["Upper_Band"], label="Upper Band", color="red", linestyle="--", alpha=0.7)
ax1.plot(df['Date'], df["Middle_Band"], label="Middle Band (SMA)", color="gray", linestyle=":", alpha=0.5)
ax1.plot(df['Date'], df["Lower_Band"], label="Lower Band", color="green", linestyle="--", alpha=0.7)
ax1.fill_between(df['Date'], df["Upper_Band"], df["Lower_Band"], color="grey", alpha=0.1, label="Volatility Band")

# Plot BUY/SELL signals
buy_signals = df[df["Signal"] == "BUY"]
sell_signals = df[df["Signal"] == "SELL"]
ax1.scatter(buy_signals['Date'], buy_signals["Close"], color="green", marker="^", s=80, label="BUY Signal", zorder=5)
ax1.scatter(sell_signals['Date'], sell_signals["Close"], color="red", marker="v", s=80, label="SELL Signal", zorder=5)

ax1.set_title(f"Tesla (TSLA) Bollinger Bands Strategy (Lookback: {lookback}, Std Dev: {std_multiplier})", fontsize=14, fontweight="bold")
ax1.set_ylabel("Price (USD)", fontsize=12)
ax1.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")

# Bottom Panel: Cumulative Returns Performance Comparison
ax2.plot(df['Date'], df['Cum_Buy_Hold'] * 100, label="Buy & Hold", color="orange", linewidth=1.5)
ax2.plot(df['Date'], df['Cum_Strategy'] * 100, label="Bollinger Bands Strategy", color="teal", linewidth=1.5)
ax2.set_title("Cumulative Returns Comparison (%)", fontsize=12, fontweight="bold")
ax2.set_xlabel("Date", fontsize=12)
ax2.set_ylabel("Cumulative Return (%)", fontsize=12)
ax2.legend(loc="upper left", frameon=True, facecolor="white", edgecolor="none")

plt.tight_layout()

plt.savefig('tesla_backtest_results.png', dpi=300)
print("Plot successfully saved to disk as 'tesla_backtest_results.png'")

plt.show() 

plt.close()