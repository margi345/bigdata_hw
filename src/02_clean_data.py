import os
import pandas as pd

# -------------------------------
# 1. Load the local raw CSV
# -------------------------------
raw_path = "data/raw/stock_market_raw.csv"

print(f"Loading raw data from: {raw_path}")
df = pd.read_csv(
    raw_path,
    na_values=["", "NA", "N/A", "null", "-"]  # normalize missing values
)

print("✅ Loaded raw data.")
print("Shape:", df.shape)

# -------------------------------
# 2. Normalize column names to snake_case
# -------------------------------
df.columns = (
    df.columns
      .str.strip()            # remove spaces around names
      .str.lower()            # lowercase
      .str.replace(" ", "_")  # spaces -> _
      .str.replace("-", "_")  # dashes -> _
)

print("\n🔹 Column names after normalization:")
print(list(df.columns))

# -------------------------------
# 3. Clean text columns: strip spaces
# -------------------------------
str_cols = df.select_dtypes(include="object").columns

for col in str_cols:
    df[col] = df[col].str.strip()

print("\n🔹 Cleaned string columns (trimmed spaces).")

# -------------------------------
# 4. Parse date column to datetime (YYYY-MM-DD)
# -------------------------------
# Adjust the name if your date column is different
date_col_candidates = [c for c in df.columns if "date" in c]

if date_col_candidates:
    date_col = date_col_candidates[0]
    print(f"\nUsing '{date_col}' as date column.")
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
else:
    print("\n⚠ No column with 'date' found! Check your data.")
    date_col = None

# -------------------------------
# 5. Convert numeric columns (best guess)
# -------------------------------
# Use your actual numeric columns
possible_numeric_cols = ["open_price", "close_price", "volume"]

for col in possible_numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        print(f"Converted '{col}' to numeric.")

print("\n🔹 Finished numeric conversions (where columns exist).")

# -------------------------------
# 6. Drop duplicate rows
# -------------------------------
before = df.shape[0]
df = df.drop_duplicates()
after = df.shape[0]

print(f"\n🔹 Dropped duplicates: {before - after} rows removed.")
print("New shape:", df.shape)

# -------------------------------
# 7. Save as cleaned.parquet
# -------------------------------
output_dir = "data/processed"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "cleaned.parquet")

df.to_parquet(output_path, index=False)
print(f"\n💾 Saved cleaned data to: {output_path}")

# Optional: quick check on types
print("\n🔹 Final dtypes:")
print(df.dtypes)
