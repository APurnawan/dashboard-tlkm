
# =========================================================
# IMPORT LIBRARY
# =========================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================================================
# CONFIG PAGE
# =========================================================

st.set_page_config(
    page_title="Dashboard TLKM",
    page_icon="📈",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1120;
    color: white;
}

.card {
    background: linear-gradient(145deg, #111827, #0f172a);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 0px 15px rgba(0,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.05);
}

.metric-title {
    font-size: 14px;
    color: #94a3b8;
}

.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("📈 Dashboard Analisis Saham TLKM")

# =========================================================
# DOWNLOAD DATA
# =========================================================

df = yf.download(
    'TLKM.JK',
    start='2023-01-01',
    end='2025-01-01'
)

# Fix MultiIndex
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Reset index
df.reset_index(inplace=True)

# Rename Date column
if 'Date' not in df.columns:
    df.rename(columns={df.columns[0]:'Date'}, inplace=True)

# =========================================================
# ANALISIS DATA
# =========================================================

# Return
df['Return'] = df['Close'].pct_change()

# Moving Average
df['MA7'] = df['Close'].rolling(7).mean()
df['MA30'] = df['Close'].rolling(30).mean()

# Volatility
df['Volatility'] = df['Return'].rolling(30).std()

# =========================================================
# METRIC CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

last_close = round(df['Close'].iloc[-1], 2)
prev_close = round(df['Close'].iloc[-2], 2)

change = round(last_close - prev_close, 2)
pct = round((change / prev_close) * 100, 2)

volume = int(df['Volume'].iloc[-1])

high52 = round(df['High'].max(), 2)
low52 = round(df['Low'].min(), 2)

with col1:

    st.markdown(f"""
    <div class="card">
        <div class="metric-title">
        Harga Terakhir
        </div>

        <div class="metric-value">
        {last_close}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class="card">
        <div class="metric-title">
        Perubahan Harian
        </div>

        <div class="metric-value">
        {pct}%
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown(f"""
    <div class="card">
        <div class="metric-title">
        Volume Trading
        </div>

        <div class="metric-value">
        {volume:,}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:

    st.markdown(f"""
    <div class="card">
        <div class="metric-title">
        52 Week High
        </div>

        <div class="metric-value">
        {high52}
        </div>

        <br>

        <div class="metric-title">
        52 Week Low
        </div>

        <div class="metric-value">
        {low52}
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CANDLESTICK CHART
# =========================================================

st.subheader("📊 Pergerakan Harga Saham")

fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.05,
    row_heights=[0.7, 0.3]
)

# Candlestick
fig.add_trace(

    go.Candlestick(

        x=df['Date'],

        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],

        increasing_line_color='#00ff99',
        decreasing_line_color='#ff4d4d',

        name='Harga'

    ),

    row=1,
    col=1
)

# MA7
fig.add_trace(

    go.Scatter(

        x=df['Date'],
        y=df['MA7'],

        line=dict(
            color='cyan',
            width=2
        ),

        name='MA7'

    ),

    row=1,
    col=1
)

# MA30
fig.add_trace(

    go.Scatter(

        x=df['Date'],
        y=df['MA30'],

        line=dict(
            color='orange',
            width=2
        ),

        name='MA30'

    ),

    row=1,
    col=1
)

# Volume
fig.add_trace(

    go.Bar(

        x=df['Date'],
        y=df['Volume'],

        marker_color='#00ccff',

        name='Volume'

    ),

    row=2,
    col=1
)

fig.update_layout(

    template='plotly_dark',

    paper_bgcolor='#0b1120',
    plot_bgcolor='#0b1120',

    height=750,

    xaxis_rangeslider_visible=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# VOLATILITY CHART
# =========================================================

st.subheader("📉 Volatilitas Saham")

fig2 = go.Figure()

fig2.add_trace(

    go.Scatter(

        x=df['Date'],
        y=df['Volatility'],

        mode='lines',

        line=dict(
            color='#39ff14',
            width=3
        ),

        fill='tozeroy'
    )
)

fig2.update_layout(

    template='plotly_dark',

    paper_bgcolor='#0b1120',
    plot_bgcolor='#0b1120',

    height=300
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =========================================================
# DATA TERBARU
# =========================================================

st.subheader("📋 Data Terbaru")

st.dataframe(
    df.tail(),
    use_container_width=True
)
