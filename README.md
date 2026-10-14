# Super Trading · Quant Assignment · Part B

**Time:** about 45 minutes. **AI:** allowed and encouraged. Tell us how you used it in the form.

You don't need any prior trading knowledge. Everything you need is on this page.

---

## The data

`nifty_5min_2025.csv` has one year of **5-minute candles** for a NIFTY-like index.

| Column | Meaning |
|---|---|
| `datetime` | Start time of the 5-minute candle (IST), e.g. `2025-01-01 09:30` covers 9:30–9:35 |
| `open` | Price at the start of the candle |
| `high` / `low` | Highest / lowest price during the candle |
| `close` | Price at the end of the candle |

The market is open from **9:15 to 15:30**, so a normal day has 75 candles (09:15 … 15:25).

The data is synthetic, but built to behave like the real thing. **Treat it like data you received from a vendor.**

---

## The strategy

Every trading day:

1. At **9:30**, compare the price with **yesterday's closing price**.
   - If today's 9:30 price is **higher** → **BUY** (you make money if the price goes up).
   - Otherwise → **SELL / short** (you make money if the price goes down).
2. At **15:15**, close the position.

Definitions:

| Term | Use this |
|---|---|
| Today's 9:30 price (entry) | `open` of the 09:30 candle |
| Exit price | `open` of the 15:15 candle |
| Yesterday's closing price | `close` of the last candle of the previous trading day |
| Position size | 1 lot = **75 units** |
| Cost | **₹40 per trade** (entry + exit together) |

P&L of one trade:

```
BUY  : (exit − entry) × 75 − 40
SELL : (entry − exit) × 75 − 40
```

---

## What to submit (in the form)

1. **Your code:** a public GitHub repo **or** a Google Colab notebook link (sharing set to "Anyone with the link can view"). Any language is fine; Python is most common.
2. **Results:**
   - Total P&L (₹)
   - Number of trades
   - Win rate (% of trades with P&L > 0)
   - Worst single day: date and P&L
   - An equity curve chart (cumulative P&L over time), in the repo/notebook
3. **Assumptions you made, and anything in the data that looked odd**, with what you did about it.
4. **Would you put real money into this strategy? Why or why not?** 3–5 lines.

We care more about **correct logic and clear reasoning** than pretty code. A short, honest answer beats a long one.
