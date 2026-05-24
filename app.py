
# =========================================================
# DASHBOARD ANALISIS SAHAM TLKM
# PREMIUM FINTECH VERSION
# =========================================================

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

/* Background utama */
.stApp {
    background-color: #0b1120;
    color: white;
}

/* Hilangkan menu bawaan */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* Container */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Card */
.card {
    background: linear-gradient(145deg, #111827, #0f172a);
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 0px 15px rgba(0,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.05);
}

/* Metric title */
.metric-title {
    font-size: 14px;
    color: #94a3b8;
}

/* Metric value */
.metric-value {
    font-size: 30px;
    font-weight: bold;
    color: white;
}

/* Metric green */
.metric-green {
    color: #22c55e;
    font-size: 18px;
}

/* Metric red */
.metric-red {
    color: #ef4444;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DOWNLOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = yf.download(
        'TLKM.JK',
        start='2023-01-01',
        end='2025-01-01'
    )

    # Fix MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Reset Index
    df.reset_index(inplace=True)

    # Rename kolom date
    if 'Date' not in df.columns:
        df.rename(columns={df.columns[0]:'Date'}, inplace=True)

    return df

df = load_data()

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
# HEADER
# =========================================================

header_left, header_right = st.columns([4,1])

with header_left:

    st.markdown("""
    <h1 style='font-size:32px; color:white; margin-bottom:0px;'>
    📈 Dashboard Analisis Saham TLKM
    </h1>
    """, unsafe_allow_html=True)

with header_right:

    st.selectbox(
        "Periode",
        ["1 Tahun", "6 Bulan", "3 Bulan"]
    )

# =========================================================
# METRIC CARDS
# =========================================================

col1, col2, col3, col4 = st.columns([1,1,1,1.2])

last_close = round(df['Close'].iloc[-1], 2)
prev_close = round(df['Close'].iloc[-2], 2)

change = round(last_close - prev_close, 2)

pct = round(
    (change / prev_close) * 100,
    2
)

volume = int(df['Volume'].iloc[-1])

high52 = round(df['High'].max(), 2)
low52 = round(df['Low'].min(), 2)

open_price = round(df['Open'].iloc[-1], 2)
high_price = round(df['High'].iloc[-1], 2)
low_price = round(df['Low'].iloc[-1], 2)

# =========================================================
# CARD 1
# =========================================================

with col1:

    st.markdown(f"""
    <div class="card">

        <div class="metric-title">
        Harga Terakhir
        </div>

        <div class="metric-value">
        {last_close}
        </div>

        <div class="metric-red">
        {change} ({pct}%)
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CARD 2
# =========================================================

with col2:

    warna = "metric-green"

    if change < 0:
        warna = "metric-red"

    st.markdown(f"""
    <div class="card">

        <div class="metric-title">
        Perubahan Hari Ini
        </div>

        <div class="metric-value">
        {pct}%
        </div>

        <div class="{warna}">
        {change}
        </div>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# CARD 3
# =========================================================

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

# =========================================================
# CARD 4
# =========================================================

with col4:

    st.markdown(f"""
    <div class="card">

        <div class="metric-title">
        Ringkasan Harga
        </div>

        <br>

        Open : {open_price}

        <br><br>

        High : {high_price}

        <br><br>

        Low : {low_price}

        <br><br>

        52W High : {high52}

        <br><br>

        52W Low : {low52}

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MAIN LAYOUT
# =========================================================

left_col, right_col = st.columns([3,1])

# =========================================================
# LEFT SIDE CHART
# =========================================================

with left_col:

    st.markdown("### 📊 Pergerakan Harga")

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25]
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

    # Layout chart
    fig.update_layout(

        template='plotly_dark',

        paper_bgcolor='#0b1120',
        plot_bgcolor='#0b1120',

        height=500,

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),

        xaxis_rangeslider_visible=False,

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# RIGHT SIDE PANEL
# =========================================================

with right_col:

    # =====================================================
    # SENTIMENT
    # =====================================================

    st.markdown("### 📈 Sentiment")

    sentiment_score = 78

    st.metric(
        label="Indikator Sentimen",
        value="BULLISH",
        delta=f"{sentiment_score}/100"
    )

    # =====================================================
    # VOLATILITY
    # =====================================================

    st.markdown("### 📉 Volatilitas")

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

        height=180,

        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        )
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # =====================================================
    # SUMBER DATA
    # =====================================================

    st.markdown("""
    <div class="card">

    <div class="metric-title">
    Sumber Data
    </div>

    <br>

    🟢 yfinance

    <br><br>

    Real-time Market Data

    </div>
    """, unsafe_allow_html=True)
