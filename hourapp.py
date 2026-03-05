import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine

# --- 1. Page Config ---
st.set_page_config(page_title="Stock Winners", layout="wide")
st.title("🏆 25-Min Bracket Winners")

# --- 2. Database Setup (In-Memory) ---
engine = create_engine('sqlite://')

stock_urls = {
  "ADANIENT": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE423A01024&interval=I1&from=1772735399999&limit=500",
"ADANIPORT": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE742F01042&interval=I1&from=1772735399999&limit=500",
"APOLLOHOSP": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE437A01024&interval=I1&from=1772735399999&limit=500",
"ASIANPAINT": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE021A01026&interval=I1&from=1772735399999&limit=500",
"AXISBANK": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE238A01034&interval=I1&from=1772735399999&limit=500",
"BAJAJAUTO": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE917I01010&interval=I1&from=1772735399999&limit=500",
"BAJAJFINSV": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE918I01026&interval=I1&from=1772735399999&limit=500",
"BAJFINANCE": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE296A01032&interval=I1&from=1772735399999&limit=500",
"BEL": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE263A01024&interval=I1&from=1772735399999&limit=500",
"BHARTIARTL": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE397D01024&interval=I1&from=1772735399999&limit=500",
"CIPLA": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE059A01026&interval=I1&from=1772735399999&limit=500",
"COALINDIA": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE522F01014&interval=I1&from=1772735399999&limit=500",
"DRREDDY": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE089A01031&interval=I1&from=1772735399999&limit=500",
"EICHER": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE066A01021&interval=I1&from=1772735399999&limit=500",
"ETERNAL": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE758T01015&interval=I1&from=1772735399999&limit=500",
"GRASIM": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE047A01021&interval=I1&from=1772735399999&limit=500",
"HCLTECH": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE860A01027&interval=I1&from=1772735399999&limit=500",
"HDFCBANK": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE040A01034&interval=I1&from=1772735399999&limit=500",
"HDFCLIFE": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE795G01014&interval=I1&from=1772735399999&limit=500",
"HEROMOTOCO": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE158A01026&interval=I1&from=1772735399999&limit=500",
"HINDALCO": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE038A01020&interval=I1&from=1772735399999&limit=500",
"HINDUNILVR": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE030A01027&interval=I1&from=1772735399999&limit=500",
"ICICIBANK": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE090A01021&interval=I1&from=1772735399999&limit=500",
"INDIGO": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE646L01027&interval=I1&from=1772735399999&limit=500",
"INDUSINDBK": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE095A01012&interval=I1&from=1772735399999&limit=500",
"INFY": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE009A01021&interval=I1&from=1772735399999&limit=500",
"ITC": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE154A01025&interval=I1&from=1772735399999&limit=500",
"JIOFIN": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE758E01017&interval=I1&from=1772735399999&limit=500",
"JSWSTEEL": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE019A01038&interval=I1&from=1772735399999&limit=500",
"KOTAKBANK": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE237A01028&interval=I1&from=1772735399999&limit=500",
"LT": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE018A01030&interval=I1&from=1772735399999&limit=500",
"MARUTI": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE585B01010&interval=I1&from=1772735399999&limit=500",
"MAXHEALTH": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE027H01010&interval=I1&from=1772735399999&limit=500",
"MM": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE101A01026&interval=I1&from=1772735399999&limit=500",
"NESTLEIND": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE239A01024&interval=I1&from=1772735399999&limit=500",
"NTPC": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE733E01010&interval=I1&from=1772735399999&limit=500",
"ONGC": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE213A01029&interval=I1&from=1772735399999&limit=500",
"POWERGRID": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE752E01010&interval=I1&from=1772735399999&limit=500",
"RELIANCE": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE002A01018&interval=I1&from=1772735399999&limit=500",
"SBILIFE": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE123W01016&interval=I1&from=1772735399999&limit=500",
"SBIN": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE062A01020&interval=I1&from=1772735399999&limit=500",
"SHRIRAMFIN": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE721A01047&interval=I1&from=1772735399999&limit=500",
"SUNPHARMA": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE044A01036&interval=I1&from=1772735399999&limit=500",
"TATACONSUM": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE192A01025&interval=I1&from=1772735399999&limit=500",
"TATAMOTORS": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE155A01022&interval=I1&from=1772735399999&limit=500",
"TATASTEEL": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE081A01020&interval=I1&from=1772735399999&limit=500",
"TCS": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE467B01029&interval=I1&from=1772735399999&limit=500",
"TECHM": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE669C01036&interval=I1&from=1772735399999&limit=500",
"TITAN": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE280A01028&interval=I1&from=1772735399999&limit=500",
"TRENT": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE849A01020&interval=I1&from=1772735399999&limit=500",
"ULTRACEMCO": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE481G01011&interval=I1&from=1772735399999&limit=500",
"WIPRO": "https://service.upstox.com/chart/open/v3/candles?instrumentKey=NSE_EQ%7CINE075A01022&interval=I1&from=1772735399999&limit=500"
}

# --- 3. Data Fetching ---
@st.cache_data(ttl=60) # Auto-refresh data every 60 seconds
def fetch_data():
    all_data = []
    for symbol, url in stock_urls.items():
        try:
            response = requests.get(url)
            raw_candles = response.json().get('data', {}).get('candles', [])
            if raw_candles:
                df = pd.DataFrame(raw_candles, columns=['ts_raw', 'open', 'high', 'low', 'close', 'volume', 'oi'])
                df['symbol'] = symbol
                all_data.append(df)
        except Exception as e:
            st.error(f"Error fetching {symbol}: {e}")
    return pd.concat(all_data) if all_data else None

raw_df = fetch_data()

if raw_df is not None:
    raw_df.to_sql('stock_minutes', engine, if_exists='replace', index=False)

# --- 4. SQL Analysis (Fixed for Time Zones) ---
    query = """
    WITH BaseData AS (
        SELECT 
            symbol,
            -- Force IST (+5.5 hours) for Streamlit Cloud servers
            datetime(ts_raw/1000.0, 'unixepoch', '+5.5 hours') as l_time,
            (volume * close) as minute_val
        FROM stock_minutes
    ),
    BracketCalc AS (
        SELECT 
            symbol, minute_val,
            ((strftime('%H', l_time) * 60 + strftime('%M', l_time)) - 555) / 25 AS bracket_id
        FROM BaseData
        WHERE bracket_id >= 0 AND bracket_id < 16
    ),
    Aggregated AS (
        SELECT 
            bracket_id, symbol, SUM(minute_val) as total_val,
            time(555 * 60 + (bracket_id * 25 * 60), 'unixepoch') || ' to ' || 
            time(555 * 60 + ((bracket_id + 1) * 25 * 60), 'unixepoch') as time_slot
        FROM BracketCalc
        GROUP BY bracket_id, symbol
    ),
    Ranked AS (
        SELECT 
            time_slot, symbol, total_val,
            RANK() OVER (PARTITION BY time_slot ORDER BY total_val DESC) as rnk
        FROM Aggregated
    )
    SELECT time_slot AS "Time Interval", symbol AS "Top Company", total_val AS "Traded Value"
    FROM Ranked WHERE rnk = 1
    ORDER BY "Time Interval" ASC;

    """
    
    winners_df = pd.read_sql(query, engine)

    # --- 5. Display Table ---
    if not winners_df.empty:
        # st.dataframe makes the table interactive (sortable)
        st.dataframe(winners_df, use_container_width=True, hide_index=True)
    else:
        st.info("Market is currently closed or data is not yet available for the 09:15 bracket.")

else:

    st.warning("Connecting to Upstox API...")




