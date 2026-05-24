import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import json
# =========================================================
# CONFIG DASHBOARD
# =========================================================

st.set_page_config(
    page_title="Dashboard Analisis Saham TLKM",
    layout="wide"
)

# =========================================================
# DATA COLLECTION
# Mengambil data saham TLKM dari Yahoo Finance
# =========================================================
# =========================================================
# PILIH PERIODE
# =========================================================

period_option = st.selectbox(

    "Pilih Periode",

    {

        "1 Tahun":"1y",
        "6 Bulan":"6mo",
        "3 Bulan":"3mo",
        "1 Bulan":"1mo"

    }

)

selected_period = {

    "1 Tahun":"1y",
    "6 Bulan":"6mo",
    "3 Bulan":"3mo",
    "1 Bulan":"1mo"

}[period_option]
df = yf.download(
    'TLKM.JK',
    period=selected_period,
    auto_adjust=True,
    progress=False
)

# =========================================================
# DATA CLEANING
# Membersihkan struktur dataframe
# =========================================================

# Fix MultiIndex
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Reset index
df.reset_index(inplace=True)

# Rename tanggal
df.rename(columns={df.columns[0]: 'Date'}, inplace=True)

# Hapus missing value
df.dropna(inplace=True)

# Hapus duplicate
df.drop_duplicates(inplace=True)

# =========================================================
# FEATURE ENGINEERING
# Membuat indikator analisis saham
# =========================================================

# Return Harian
df['Return'] = df['Close'].pct_change()

# Moving Average
df['MA7'] = df['Close'].rolling(7).mean()

df['MA30'] = df['Close'].rolling(30).mean()

# Volatility
df['Volatility'] = df['Return'].rolling(30).std()

# =========================================================
# BUY SELL SIGNAL
# =========================================================

df['Signal'] = np.where(
    df['MA7'] > df['MA30'],
    'BUY',
    'SELL'
)

latest_signal = df['Signal'].iloc[-1]

# =========================================================
# METRIC ANALYSIS
# =========================================================

last_close = round(df['Close'].iloc[-1],2)

prev_close = round(df['Close'].iloc[-2],2)

change_value = round(last_close - prev_close,2)

pct = round((change_value / prev_close) * 100,2)

change = f"{change_value} ({pct}%)"

volume = int(float(df['Volume'].iloc[-1]))

open_price = round(df['Open'].iloc[-1],2)

high_price = round(df['High'].iloc[-1],2)

low_price = round(df['Low'].iloc[-1],2)

close_price = round(df['Close'].iloc[-1],2)

high52 = round(df['High'].max(),2)

low52 = round(df['Low'].min(),2)

volatility = round(df['Volatility'].iloc[-1],4)

# =========================================================
# CHART DATA
# =========================================================

labels = df['Date'].dt.strftime('%b').tolist()

close_data = df['Close'].tolist()

ma7_data = df['MA7'].tolist()

ma30_data = df['MA30'].tolist()

volume_data = df['Volume'].tolist()

volatility_data = df['Volatility'].tolist()

# FIX NaN
close_data = [None if pd.isna(x) else x for x in close_data]

ma7_data = [None if pd.isna(x) else x for x in ma7_data]

ma30_data = [None if pd.isna(x) else x for x in ma30_data]

volume_data = [None if pd.isna(x) else x for x in volume_data]

volatility_data = [
    None if pd.isna(x) else x
    for x in volatility_data
]
# =========================================================
# INSIGHT ANALYSIS
# =========================================================

if latest_signal == 'BUY':
    insight = """
    Tren saham TLKM saat ini menunjukkan sinyal bullish.
    Moving Average 7 hari berada di atas MA30 yang
    mengindikasikan potensi kenaikan harga.
    """
else:
    insight = """
    Tren saham TLKM saat ini menunjukkan sinyal bearish.
    Moving Average 7 hari berada di bawah MA30 yang
    mengindikasikan tekanan penurunan harga.
    """

# =========================================================
# LOAD HTML TEMPLATE
# =========================================================

with open("template.html","r",encoding="utf-8") as f:

    html = f.read()

# =========================================================
# REPLACE METRIC TEXT
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

html = html.replace("{{signal}}", latest_signal)

html = html.replace("{{insight}}", insight)

# =========================================================
# REPLACE CHART DATA
# =========================================================

import json

html = html.replace(
    "{{labels}}",
    json.dumps(labels)
)

html = html.replace(
    "{{close_data}}",
    json.dumps(close_data)
)

html = html.replace(
    "{{ma7_data}}",
    json.dumps(ma7_data)
)

html = html.replace(
    "{{ma30_data}}",
    json.dumps(ma30_data)
)

html = html.replace(
    "{{volume_data}}",
    json.dumps(volume_data)
)

html = html.replace(
    "{{volatility_data}}",
    json.dumps(volatility_data)
)
# =========================================================
# DISPLAY DASHBOARD
# =========================================================

components.html(
    html,
    height=1000,
    scrolling=False
)
