import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Dashboard TLKM",
    layout="wide"
)

# =========================================================
# DOWNLOAD DATA
# =========================================================

df = yf.download(
    'TLKM.JK',
    period='1y',
    auto_adjust=True,
    progress=False
)
# Fix MultiIndex
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Reset index
df.reset_index(inplace=True)
# =========================================================
# ANALISIS
# =========================================================

last_close = round(df['Close'].iloc[-1],2)

prev_close = round(df['Close'].iloc[-2],2)

change_value = round(last_close-prev_close,2)

pct = round((change_value/prev_close)*100,2)

change = f"{change_value} ({pct}%)"

volume = int(float(df['Volume'].iloc[-1]))

open_price = round(df['Open'].iloc[-1],2)

high_price = round(df['High'].iloc[-1],2)

low_price = round(df['Low'].iloc[-1],2)

close_price = round(df['Close'].iloc[-1],2)

high52 = round(df['High'].max(),2)

low52 = round(df['Low'].min(),2)

# =========================================================
# VOLATILITY
# =========================================================

df['Return'] = df['Close'].pct_change()

df['Volatility'] = df['Return'].rolling(30).std()

volatility = round(df['Volatility'].iloc[-1],4)

# =========================================================
# LOAD HTML
# =========================================================

with open("template.html","r",encoding="utf-8") as f:

    html = f.read()

# =========================================================
# REPLACE PLACEHOLDER
# =========================================================

html = html.replace("{{last_close}}", str(last_close))

html = html.replace("{{pct}}", str(pct)+"%")

html = html.replace("{{change}}", change)

html = html.replace("{{volume}}", f"{volume:,}")

html = html.replace("{{open}}", str(open_price))

html = html.replace("{{high}}", str(high_price))

html = html.replace("{{low}}", str(low_price))

html = html.replace("{{close}}", str(close_price))

html = html.replace("{{high52}}", str(high52))

html = html.replace("{{low52}}", str(low52))

html = html.replace("{{volatility}}", str(volatility))

# =========================================================
# DISPLAY HTML
# =========================================================
# =========================================================
# CHART DATA
# =========================================================

df['MA7'] = df['Close'].rolling(7).mean()

df['MA30'] = df['Close'].rolling(30).mean()

labels = df['Date'].dt.strftime('%b').tolist()

close_data = df['Close'].fillna(0).tolist()

ma7_data = df['MA7'].fillna(0).tolist()

ma30_data = df['MA30'].fillna(0).tolist()

volume_data = df['Volume'].fillna(0).tolist()

# =========================================================
# REPLACE CHART DATA
# =========================================================

html = html.replace(
    "{{labels}}",
    str(labels)
)

html = html.replace(
    "{{close_data}}",
    str(close_data)
)

html = html.replace(
    "{{ma7_data}}",
    str(ma7_data)
)

html = html.replace(
    "{{ma30_data}}",
    str(ma30_data)
)

html = html.replace(
    "{{volume_data}}",
    str(volume_data)
)
components.html(
    html,
    height=950,
    scrolling=False
)
