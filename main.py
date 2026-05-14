import os
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# --- TERMINAL UI CONFIGURATION ---
st.set_page_config(page_title="Ratio Analysis", page_icon="📈", layout="wide")

st.markdown("""
    <style>
    header[data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Inter', sans-serif; }

    /* Title - Fixed to Title Case with exact styling */
    .main-title {
        font-weight: 800;
        font-size: 3.2rem;
        text-align: center;
        margin-top: -45px;
        margin-bottom: 45px;
        color: #f0f6fc;
        letter-spacing: -1px;
        background: linear-gradient(180deg, #ffffff 0%, #c9d1d9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    section[data-testid="stSidebar"] { background-color: #010409 !important; border-right: 1px solid #30363d; }

    .pane-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #8b949e;
        border-bottom: 1px solid #30363d;
        padding-bottom: 5px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    div[data-testid="stMetric"] { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; }
    div[data-testid="stMetricValue"] { color: #ffffff !important; font-size: 1.8rem !important; font-weight: 700 !important; }

    .stButton>button {
        width: 100%;
        background: linear-gradient(180deg, #2ea043 0%, #238636 100%);
        color: white;
        border-radius: 6px;
        font-weight: 700;
        border: none;
        padding: 12px;
    }

    .custom-footer {
        margin-top: 100px;
        padding-bottom: 40px;
        border-top: 1px solid #30363d;
        padding-top: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### 🛠 System")
    with st.expander("🔑 API Settings", expanded=False):
        groq_key = st.text_input("Groq Node", type="password")
        serper_key = st.text_input("Serper Node", type="password")

    st.divider()
    st.markdown("### 🎯 Targeting")
    ticker = st.text_input("Enter Symbol", value="BZ=F").upper()
    time_period = st.select_slider("History Range", options=["1mo", "3mo", "6mo", "1y"], value="3mo")

    st.divider()
    run_scan = st.button("Execute System Scan")

# --- MAIN INTERFACE ---
st.markdown('<h1 class="main-title">Stock Market Ratio Analysis</h1>', unsafe_allow_html=True)

left_col, right_col = st.columns([1.3, 1], gap="large")

with left_col:
    st.markdown(f'<p class="pane-title">Quantitative Analysis: {ticker}</p>', unsafe_allow_html=True)
    try:
        data = yf.download(ticker, period="1y", interval="1d")
        if not data.empty:
            # Indicators
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            data['RSI'] = 100 - (100 / (1 + (gain / loss)))
            data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
            data['MA20'] = data['Close'].rolling(window=20).mean()
            data['STD'] = data['Close'].rolling(window=20).std()
            data['Upper'] = data['MA20'] + (data['STD'] * 2)
            data['Lower'] = data['MA20'] - (data['STD'] * 2)

            days = 30 if time_period == "1mo" else 90 if time_period == "3mo" else 180 if time_period == "6mo" else 365
            display_data = data.tail(days)

            curr = display_data['Close'].iloc[-1].item()
            diff_pct = ((curr - display_data['Close'].iloc[-2].item()) / display_data['Close'].iloc[-2].item()) * 100

            m1, m2, m3 = st.columns(3)
            m1.metric("PRICE", f"{curr:,.2f}", f"{diff_pct:+.2f}%")
            m2.metric("RSI (14)", f"{display_data['RSI'].iloc[-1]:.1f}")
            m3.metric("EMA 20", f"{display_data['EMA20'].iloc[-1]:,.2f}")

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(x=display_data.index, y=display_data['Upper'], line=dict(color='rgba(88, 166, 255, 0.1)'),
                           showlegend=False))
            fig.add_trace(
                go.Scatter(x=display_data.index, y=display_data['Lower'], line=dict(color='rgba(88, 166, 255, 0.1)'),
                           fill='tonexty', fillcolor='rgba(88, 166, 255, 0.05)', name="Volatility Zone"))
            fig.add_trace(go.Candlestick(x=display_data.index, open=display_data['Open'], high=display_data['High'],
                                         low=display_data['Low'], close=display_data['Close'], name="Price Action"))
            fig.add_trace(go.Scatter(x=display_data.index, y=display_data['EMA20'], line=dict(color='#ff7f0e', width=2),
                                     name="EMA 20"))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              height=500, xaxis_rangeslider_visible=False, margin=dict(t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Error: {e}")

with right_col:
    st.markdown('<p class="pane-title">AI Agent Strategic Stream</p>', unsafe_allow_html=True)
    if run_scan:
        if not (groq_key and serper_key):
            st.warning("API keys required.")
        else:
            os.environ["SERPER_API_KEY"] = serper_key
            llm_node = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_key, temperature=0.1)
            officer = Agent(role='Senior Analyst', goal=f'Brief on {ticker}', backstory='Expert analyst.',
                            tools=[SerperDevTool()], llm=llm_node)
            task = Task(description=f"Quick briefing for {ticker}.", expected_output="Analysis.", agent=officer)
            with st.status("📡 Processing...") as status:
                crew = Crew(agents=[officer], tasks=[task])
                output = crew.kickoff()
                status.update(label="Stream Live", state="complete")
            st.markdown(
                f'<div style="background-color: #161b22; padding: 25px; border-radius: 10px; border: 1px solid #30363d; min-height: 480px;">{output.raw}</div>',
                unsafe_allow_html=True)
    else:
        st.info("System Ready. Execute scan to initiate AI triage.")

# --- FOOTER ---
st.markdown('<div class="custom-footer">', unsafe_allow_html=True)
footer_html = f"""
<div style="text-align: center;">
    <p style="margin-bottom: 10px; font-size: 0.9rem; color: #8b949e;">Developed by <b>Hassan Moosavi</b></p>
    <div style="display: flex; justify-content: center; gap: 15px;">
        <a href="https://wa.me/31685529172" target="_blank"><img src="https://img.shields.io/badge/WhatsApp-25D366?style=flat-square&logo=whatsapp&logoColor=white" height="25"></a>
        <a href="http://linkedin.com/in/hassan-moosavi" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white" height="25"></a>
        <a href="mailto:s.h.mousaviy@gmail.com"><img src="https://img.shields.io/badge/Email-D14836?style=flat-square&logo=gmail&logoColor=white" height="25"></a>
    </div>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)