import pandas as pd
import os

# 1) Raw CSV URL
url = "https://raw.githubusercontent.com/gchandra10/filestorage/refs/heads/main/stock_market.csv"

# 2) Read CSV from URL
df = pd.read_csv(
    url,
    na_values=["", "NA", "N/A", "null", "-"]  # treat these as missing
)

print("✅ Loaded raw CSV")
print("Shape:", df.shape)

print("\n🔹 First 5 rows:")
print(df.head())

print("\n🔹 Info (dtypes + non-nulls):")
print(df.info())

print("\n🔹 Null counts per column:")
print(df.isna().sum())

# 3) OPTIONAL: save a local copy of the raw CSV (good for repo)
os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/stock_market_raw.csv", index=False)
print("\n💾 Saved local raw copy to data/raw/stock_market_raw.csv")
