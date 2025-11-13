📘 Stock Market Data Pipeline & Streamlit Dashboard

This project demonstrates a complete data engineering workflow using Python, Pandas, Parquet, and Streamlit.
The assignment includes:

Loading and inspecting raw stock market data

Cleaning and normalizing the schema

Storing cleaned data in Parquet format

Creating analytical aggregations

Building an interactive Streamlit dashboard with filters and charts

1. Data Loading & Inspection (src/01_load.py)

Loads raw CSV from GitHub

Normalizes missing values ("", NA, N/A, null, -)

Displays:

shape

head()

info()

null counts

Saves a local raw copy to:

data/raw/stock_market_raw.csv

2. Data Cleaning & Schema Normalization (src/02_clean_data.py)

Cleaning steps performed:

✔ Convert column names to snake_case

Example: Trade Date → trade_date

✔ Standardize text fields

Strip spaces

Normalize casing

Convert empty strings to NULL

✔ Convert numeric columns to float
open_price, close_price, volume

✔ Parse dates into proper datetime
trade_date → YYYY-MM-DD

✔ Deduplicate rows
✔ Save final clean file to Parquet

Final output:

data/processed/cleaned.parquet

📊 3. Aggregations (src/03_make_aggs.py)

Creates three analytics datasets:

Agg1 — Daily average close price by ticker

Saved to:

data/agg/agg1_daily_avg_close_by_ticker.parquet

Agg2 — Average volume by ticker

Saved to:

data/agg/agg2_avg_volume_by_ticker.parquet

Agg3 — Daily return percentage by ticker

Computed as:

pct_change(close_price)


Saved to:

data/agg/agg3_daily_return_by_ticker.parquet

📊 4. Streamlit Dashboard (app.py)

Interactive dashboard features:

✔ Sidebar Filters

Date range (trade_date)

Ticker multiselect

✔ Charts

Line chart: Daily average close price by ticker

Bar chart: Average volume by ticker

Line chart: Daily returns

Data table: Filtered raw data

✔ How to run:
streamlit run app.py


The app opens at:

👉 http://localhost:8501

5. Screenshots:
## 📸 Screenshots

### 📊 Default Dashboard View
![Dashboard](screenshots\dashboard.png)

### 📉 Average Volume by Ticker
![Average Volume](screenshots\average_volumebyticker.png)

### 📅 Date Range & Ticker Filter
![Date Filter](screenshots\diffrentdaterange andticker.png)


