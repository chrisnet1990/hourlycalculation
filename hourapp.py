import streamlit as st
import pandas as pd
import requests
from sqlalchemy import create_engine
import datetime

# --- 1. Page Config ---
st.set_page_config(page_title="Stock Winners", layout="wide")
st.title("🏆 Top 5 Traded Stocks per 15-Min Interval")

# --- 2. Date Selection Widget ---
# Default date can be set or derived; using a standard picker here
selected_date = st.date_input(
    "Select Trading Date", 
    value=datetime.date(2026, 6, 3) # You can adjust the default date as needed
)

# Convert the selected date to epoch time in milliseconds (start of the day)
dt = datetime.datetime.combine(selected_date, datetime.datetime.min.time())
epoch_from = int(dt.timestamp() * 1000)

# --- 3. Database Setup & Dynamic URL Mapping ---
engine = create_engine('sqlite://')

# Mapping of stock symbols to their respective Upstox instrument keys
instruments = {
    "ADANIENT": "NSE_EQ%7CINE423A01024",
    "ADANIPORT": "NSE_EQ%7CINE742F01042",
    "APOLLOHOSP": "NSE_EQ%7CINE437A01024",
    "ASIANPAINT": "NSE_EQ%7CINE021A01026",
    "AXISBANK": "NSE_EQ%7CINE238A01034",
    "BAJAJAUTO": "NSE_EQ%7CINE917I01010",
    "BAJAJFINSV": "NSE_EQ%7CINE918I01026",
    "BAJFINANCE": "NSE_EQ%7CINE296A01032",
    "BEL": "NSE_EQ%7CINE263A01024",
    "BHARTIARTL": "NSE_EQ%7CINE397D01024",
    "CIPLA": "NSE_EQ%7CINE059A01026",
    "COALINDIA": "NSE_EQ%7CINE522F01014",
    "DRREDDY": "NSE_EQ%7CINE089A01031",
    "EICHER": "NSE_EQ%7CINE066A01021",
    "ETERNAL": "NSE_EQ%7CINE758T01015",
    "GRASIM": "NSE_EQ%7CINE047A01021",
    "HCLTECH": "NSE_EQ%7CINE860A01027",
    "HDFCBANK": "NSE_EQ%7CINE040A01034",
    "HDFCLIFE": "NSE_EQ%7CINE795G01014",
    "HEROMOTOCO": "NSE_EQ%7CINE158A01026",
    "HINDALCO": "NSE_EQ%7CINE038A01020",
    "HINDUNILVR": "NSE_EQ%7CINE030A01027",
    "ICICIBANK": "NSE_EQ%7CINE090A01021",
    "INDIGO": "NSE_EQ%7CINE646L01027",
    "INDUSINDBK": "NSE_EQ%7CINE095A01012",
    "INFY": "NSE_EQ%7CINE009A01021",
    "ITC": "NSE_EQ%7CINE154A01025",
    "JIOFIN": "NSE_EQ%7CINE758E01017",
    "JSWSTEEL": "NSE_EQ%7CINE019A01038",
    "KOTAKBANK": "NSE_EQ%7CINE237A01028",
    "LT": "NSE_EQ%7CINE018A01030",
    "MARUTI": "NSE_EQ%7CINE585B01010",
    "MAXHEALTH": "NSE_EQ%7CINE027H01010",
    "MM": "NSE_EQ%7CINE101A01026",
    "NESTLEIND": "NSE_EQ%7CINE239A01024",
    "NTPC": "NSE_EQ%7CINE733E01010",
    "ONGC": "NSE_EQ%7CINE213A01029",
    "POWERGRID": "NSE_EQ%7CINE752E01010",
    "RELIANCE": "NSE_EQ%7CINE002A01018",
    "SBILIFE": "NSE_EQ%7CINE123W01016",
    "SBIN": "NSE_EQ%7CINE062A01020",
    "SHRIRAMFIN": "NSE_EQ%7CINE721A01047",
    "SUNPHARMA": "NSE_EQ%7CINE044A01036",
    "TATACONSUM": "NSE_EQ%7CINE192A01025",
    "TATAMOTORS": "NSE_EQ%7CINE155A01022",
    "TATASTEEL": "NSE_EQ%7CINE081A01020",
    "TCS": "NSE_EQ%7CINE467B01029",
    "TECHM": "NSE_EQ%7CINE669C01036",
    "TITAN": "NSE_EQ%7CINE280A01028",
    "TRENT": "NSE_EQ%7CINE849A01020",
    "ULTRACEMCO": "NSE_EQ%7CINE481G01011",
    "WIPRO": "NSE_EQ%7CINE075A01022"
}

# Dynamically construct the stock URLs using the selected epoch timestamp
stock_urls = {}
for symbol, key in instruments.items():
    if key:
        stock_urls[symbol] = f"https://service.upstox.com/chart/open/v3/candles?instrumentKey={key}&interval=I1&from={epoch_from}&limit=500"
    else:
        stock_urls[symbol] = f"https://service.upstox.com/chart/open/v3/candles?interval=I1&from={epoch_from}&limit=500"

# --- 4. Data Fetching ---
@st.cache_data(ttl=60)
def fetch_data(epoch_val):
    all_data = []
    # Re-build URLs inside or reference global stock_urls dependent on epoch_from
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

raw_df = fetch_data(epoch_from)

if raw_df is not None and not raw_df.empty:
    raw_df.to_sql('stock_minutes', engine, if_exists='replace', index=False)

    # --- 5. SQL Analysis ---
    query = """
    WITH BaseData AS (
        SELECT 
            symbol,
            open,
            close,
            datetime(ts_raw/1000.0, 'unixepoch', '+5.5 hours') as l_time,
            (volume * close) as minute_val
        FROM stock_minutes
    ),
    BracketCalc AS (
        SELECT 
            symbol, open, close, minute_val, l_time,
            ((strftime('%H', l_time) * 60 + strftime('%M', l_time)) - 555) / 15 AS bracket_id
        FROM BaseData
        WHERE bracket_id >= 0 AND bracket_id < 25
    ),
    PricePoints AS (
        SELECT 
            bracket_id, 
            symbol, 
            minute_val,
            FIRST_VALUE(open) OVER (PARTITION BY bracket_id, symbol ORDER BY l_time) as b_open,
            LAST_VALUE(close) OVER (PARTITION BY bracket_id, symbol ORDER BY l_time ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as b_close
        FROM BracketCalc
    ),
    Aggregated AS (
        SELECT 
            bracket_id, symbol, SUM(minute_val) as total_val, b_open, b_close,
            time(555 * 60 + (bracket_id * 15 * 60), 'unixepoch') || ' to ' || 
            time(555 * 60 + ((bracket_id + 1) * 15 * 60), 'unixepoch') as time_slot
        FROM PricePoints
        GROUP BY bracket_id, symbol
    ),
    Ranked AS (
        SELECT 
            time_slot, 
            symbol, 
            total_val, 
            b_open, 
            b_close,
            RANK() OVER (PARTITION BY time_slot ORDER BY total_val DESC) as rnk
        FROM Aggregated
    )
    SELECT 
        time_slot AS "Time Interval", 
        rnk,
        symbol, 
        ROUND(total_val / 10000000.0, 2) AS val_cr,
        CASE 
            WHEN b_close > b_open THEN '🟢'
            WHEN b_close < b_open THEN '🔴'
            ELSE '⚪'
        END AS trend
    FROM Ranked 
    WHERE rnk <= 5
    ORDER BY "Time Interval" ASC, rnk ASC;
    """
    
    raw_winners_df = pd.read_sql(query, engine)

    # --- 6. Format & Pivot to Wide Layout ---
    if not raw_winners_df.empty:
        raw_winners_df['stock_info'] = (
            raw_winners_df['symbol'] + 
            " (₹ " + raw_winners_df['val_cr'].apply(lambda x: f"{x:,.2f}") + " Cr) " + 
            raw_winners_df['trend']
        )
        
        pivoted_df = raw_winners_df.pivot(index='Time Interval', columns='rnk', values='stock_info').reset_index()
        
        pivoted_df = pivoted_df.rename(columns={
            1: "Top 1",
            2: "Top 2",
            3: "Top 3",
            4: "Top 4",
            5: "Top 5"
        })

        st.dataframe(pivoted_df, use_container_width=True, hide_index=True)
    else:
        st.info("Market is closed or data is not yet available for the selected date.")

else:
    st.warning("Connecting to Upstox API or no data found for the selected date...")
