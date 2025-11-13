import os
import pandas as pd

# ---------------------------------
# 1. Load cleaned parquet
# ---------------------------------
cleaned_path = "data/processed/cleaned.parquet"
print(f"Loading cleaned data from: {cleaned_path}")
df = pd.read_parquet(cleaned_path)

print("✅ Loaded cleaned data.")
print("Shape:", df.shape)

os.makedirs("data/agg", exist_ok=True)

cols = df.columns
print("\nAvailable columns:", list(cols))

# Map your actual column names
DATE_COL = "trade_date"
TICKER_COL = "ticker"
CLOSE_COL = "close_price"
VOLUME_COL = "volume"

# ---------------------------------
# 2. Aggregation 1: Daily avg close_price by ticker
# ---------------------------------
if {DATE_COL, TICKER_COL, CLOSE_COL}.issubset(cols):
    agg1 = (
        df.groupby([DATE_COL, TICKER_COL], as_index=False)[CLOSE_COL]
          .mean()
          .rename(columns={CLOSE_COL: "avg_close_price"})
    )

    agg1_path = "data/agg/agg1_daily_avg_close_by_ticker.parquet"
    agg1.to_parquet(agg1_path, index=False)
    print(f"\n💾 Saved agg1 → {agg1_path}")
else:
    print(f"\n⚠ Skipping agg1: need columns '{DATE_COL}', '{TICKER_COL}', '{CLOSE_COL}'.")

# ---------------------------------
# 3. Aggregation 2: Average volume by ticker
# ---------------------------------
if {TICKER_COL, VOLUME_COL}.issubset(cols):
    agg2 = (
        df.groupby(TICKER_COL, as_index=False)[VOLUME_COL]
          .mean()
          .rename(columns={VOLUME_COL: "avg_volume"})
    )

    agg2_path = "data/agg/agg2_avg_volume_by_ticker.parquet"
    agg2.to_parquet(agg2_path, index=False)
    print(f"💾 Saved agg2 → {agg2_path}")
else:
    print(f"\n⚠ Skipping agg2: need columns '{TICKER_COL}', '{VOLUME_COL}'.")

# ---------------------------------
# 4. Aggregation 3: Daily return by ticker
# ---------------------------------
if {DATE_COL, TICKER_COL, CLOSE_COL}.issubset(cols):
    df_sorted = df.sort_values([TICKER_COL, DATE_COL])

    df_sorted["daily_return"] = (
        df_sorted.groupby(TICKER_COL)[CLOSE_COL].pct_change()
    )

    agg3 = df_sorted[[DATE_COL, TICKER_COL, "daily_return"]].dropna()

    agg3_path = "data/agg/agg3_daily_return_by_ticker.parquet"
    agg3.to_parquet(agg3_path, index=False)
    print(f"💾 Saved agg3 → {agg3_path}")
else:
    print(f"\n⚠ Skipping agg3: need columns '{DATE_COL}', '{TICKER_COL}', '{CLOSE_COL}'.")

print("\n✅ Aggregation step finished.")
