# Bollinger-Band-Strategy
The Bollinger Bands  strategy operates on the core financial principle that asset prices tend to return to their historical average after extreme movements. By tracking a central moving average alongside two outer statistical boundaries set by market volatility , the bands expand during chaotic trading and contract during quiet periods.

The strategy relies on the statistical concept of mean reversion, assuming that asset prices tend to return to their historical average over time. 

1. **Volatility Channels:** The system calculates a moving baseline accompanied by upper and lower bands set at a distance proportional to market volatility (Standard Deviation).
2. **Buy Signal (Long Entry):** Triggered when the asset price drops below the **Lower Band**, indicating an oversold condition primed for a correction upward.
3. **Sell Signal (Short Entry / Take Profit):** Triggered when the asset price surges past the **Upper Band**, indicating an overbought condition likely to experience a pullback.
4. **Hold State:** Activated when the price remains structurally stable within the parameters of the inner bands.

---

## Technical Formula

The components are calculated dynamically based on a customizable lookback period ($n$) and standard deviation multiplier ($k$):

* **Middle Band (\text{MB}):** \text{MB} = \frac{1}{n} \sum_{i=1}^{n} \text{Close}_i

* **Upper Band (\text{UB}):** \text{UB} = \text{MB} + (k \times \sigma)

* **Lower Band (\text{LB}):** \text{LB} = \text{MB} - (k \times \sigma)

*Where sigma represents the n_period standard deviation of the closing price.*

---

## Core Features

- **Vectorized Execution:** Uses `numpy.select` for rapid signal assignment without slow iterative loops, making it highly suitable for large historical datasets.
- **Look-Ahead Bias Prevention:** Designed to evaluate conditions efficiently using clean mathematical logic.
- **Minimal Dependencies:** Built strictly on top of standard analytical packages (`pandas`, `numpy`).

---

## Quick Start & Code Example

Ensure you have your environment set up with:
```bash
pip install pandas numpy
