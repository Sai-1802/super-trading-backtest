
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("nifty_5min_2025.csv")

# Convert datetime column
df["datetime"] = pd.to_datetime(df["datetime"])

# Remove duplicate timestamps, keeping the first row
df = df.drop_duplicates(subset="datetime", keep="first").copy()

df["date"] = df["datetime"].dt.date
df["time"] = df["datetime"].dt.strftime("%H:%M")

# Get the last candle close for each trading day
daily_close = (
    df.sort_values("datetime")
    .groupby("date")
    .tail(1)
    .set_index("date")["close"]
)

# Entry at 09:30 and exit at 15:15
entries = df[df["time"] == "09:30"].set_index("date")["open"]
exits = df[df["time"] == "15:15"].set_index("date")["open"]

trades = []

for day in sorted(set(entries.index) & set(exits.index)):
    previous_days = [d for d in daily_close.index if d < day]

    if not previous_days:
        continue

    previous_day = max(previous_days)

    entry = float(entries.loc[day])
    exit_price = float(exits.loc[day])
    previous_close = float(daily_close.loc[previous_day])

    # Buy if entry is above yesterday's close; otherwise sell
    side = "BUY" if entry > previous_close else "SELL"

    if side == "BUY":
        pnl = (exit_price - entry) * 75 - 40
    else:
        pnl = (entry - exit_price) * 75 - 40

    trades.append({
        "date": str(day),
        "side": side,
        "entry": entry,
        "exit": exit_price,
        "pnl": pnl
    })

# Stop if no valid trades were found
if not trades:
    raise ValueError("No valid trades found. Check the CSV file and candle times.")

results = pd.DataFrame(trades)
results["cumulative_pnl"] = results["pnl"].cumsum()

# Calculate required metrics
total_pnl = results["pnl"].sum()
number_of_trades = len(results)
win_rate = (results["pnl"] > 0).mean() * 100
worst_day = results.loc[results["pnl"].idxmin()]

print("\n--- BACKTEST RESULTS ---")
print("Total P&L (₹):", total_pnl)
print("Number of trades:", number_of_trades)
print("Win rate (%):", win_rate)
print("Worst single day: date:", worst_day["date"])
print("Worst single day: P&L (₹):", worst_day["pnl"])

# Save individual trade results
results.to_csv("trade_results.csv", index=False)
print("\nSaved trade_results.csv")

# Plot and save equity curve
plt.figure(figsize=(11, 5.5))
plt.plot(
    pd.to_datetime(results["date"]),
    results["cumulative_pnl"]
)
plt.axhline(0, linewidth=1)
plt.title("Equity Curve - NIFTY Strategy 2025")
plt.xlabel("Date")
plt.ylabel("Cumulative P&L (₹)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("equity_curve.png", dpi=160)
plt.show()

print("Saved equity_curve.png")
