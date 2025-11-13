import pandas as pd
import streamlit as st
from pathlib import Path

# -----------------------------------
# Paths
# -----------------------------------
DATA_DIR = Path("data")
PROCESSED_DIR = DATA_DIR / "processed"
AGG_DIR = DATA_DIR / "agg"

# -----------------------------------
# Load data (with caching)
# -----------------------------------
@st.cache_data
def load_data():
    cleaned = pd.read_parquet(PROCESSED_DIR / "cleaned.parquet")
    agg1 = pd.read_parquet(AGG_DIR / "agg1_daily_avg_close_by_ticker.parquet")
    agg2 = pd.read_parquet(AGG_DIR / "agg2_avg_volume_by_ticker.parquet")
    agg3 = pd.read_parquet(AGG_DIR / "agg3_daily_return_by_ticker.parquet")

    # Make sure dates are datetime
    for df in (cleaned, agg1, agg3):
        if "trade_date" in df.columns:
            df["trade_date"] = pd.to_datetime(df["trade_date"])

    return cleaned, agg1, agg2, agg3


cleaned, agg1, agg2, agg3 = load_data()

# -----------------------------------
# App title
# -----------------------------------
st.title("Stock Market Dashboard")

st.write(
    "This dashboard uses cleaned stock market data and precomputed aggregations "
    "stored in Parquet format."
)

# -----------------------------------
# Sidebar filters
# -----------------------------------
st.sidebar.header("Filters")

# Date range filter
min_date = cleaned["trade_date"].min().date()
max_date = cleaned["trade_date"].max().date()

date_range = st.sidebar.date_input(
    "Trade date range",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, tuple):
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# Ticker filter
all_tickers = sorted(
    cleaned["ticker"].dropna().unique().tolist()
)

selected_tickers = st.sidebar.multiselect(
    "Select tickers",
    options=all_tickers,
    default=all_tickers[:3] if len(all_tickers) > 3 else all_tickers,
)

# If nothing selected, show all
if not selected_tickers:
    selected_tickers = all_tickers

# -----------------------------------
# Apply filters
# -----------------------------------
def filter_by_date_ticker(df, date_col="trade_date"):
    out = df.copy()
    out = out[
        (out[date_col].dt.date >= start_date)
        & (out[date_col].dt.date <= end_date)
        & (out["ticker"].isin(selected_tickers))
    ]
    return out


filtered_cleaned = filter_by_date_ticker(cleaned)
filtered_agg1 = filter_by_date_ticker(agg1)
filtered_agg3 = filter_by_date_ticker(agg3)

# -----------------------------------
# Summary section
# -----------------------------------
st.subheader("Summary")

st.write(
    f"Showing data from **{start_date}** to **{end_date}** "
    f"for tickers: {', '.join(selected_tickers)}"
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rows in filtered data", len(filtered_cleaned))

with col2:
    st.metric("Unique tickers", filtered_cleaned["ticker"].nunique())

with col3:
    st.metric("Total volume", int(filtered_cleaned["volume"].sum()))

# -----------------------------------
# Chart 1: Daily average close price by ticker
# -----------------------------------
st.subheader("Daily Average Close Price by Ticker")

if not filtered_agg1.empty:
    # Pivot so each ticker is a separate line
    pivot_avg_close = filtered_agg1.pivot_table(
        index="trade_date",
        columns="ticker",
        values="avg_close_price",
    )
    st.line_chart(pivot_avg_close)
else:
    st.info("No data available for the selected filters.")

# -----------------------------------
# Chart 2: Average volume by ticker (bar chart)
# -----------------------------------
st.subheader("Average Volume by Ticker")

avg_vol_filtered = (
    agg2[agg2["ticker"].isin(selected_tickers)]
    .set_index("ticker")
    .sort_values("avg_volume", ascending=False)
)

if not avg_vol_filtered.empty:
    st.bar_chart(avg_vol_filtered["avg_volume"])
else:
    st.info("No volume data for the selected tickers.")

# -----------------------------------
# Chart 3: Daily return by ticker
# -----------------------------------
st.subheader("Daily Return by Ticker")

if not filtered_agg3.empty:
    pivot_return = filtered_agg3.pivot_table(
        index="trade_date",
        columns="ticker",
        values="daily_return",
    )
    st.line_chart(pivot_return)
else:
    st.info("No daily return data for the selected filters.")

# -----------------------------------
# Raw data section (optional)
# -----------------------------------
with st.expander("Show raw filtered data"):
    st.dataframe(filtered_cleaned)
