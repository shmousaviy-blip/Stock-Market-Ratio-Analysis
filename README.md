# Stock Market Ratio Analysis

> A dual-engine financial terminal that fuses quantitative technical indicators with live multi-agent AI market intelligence.

---

## 🚀 Overview

The **Stock Market Ratio Analysis Terminal** is a high-performance financial dashboard engineered to provide traders, quants, and asset managers with instantaneous quantitative metrics alongside context-aware macro analyses. Designed with a sleek, low-latency dark-themed terminal UI, this platform eliminates the gap between raw data parsing and actionable investment strategies.

---

## ⚡ Key Technical Features

* **Quantitative Analytics & Volatility Tracking:** Integrates dynamic price action tracking using standard `yfinance` architecture. It calculates real-time Exponential Moving Averages (EMA 20), Relative Strength Index (RSI 14), and maps custom-rendered Bollinger Bands (**Volatility Zone**) to isolate key price violations and market anomalies.
* **Multi-Agent AI Strategic Triage:** Built on top of the `CrewAI` framework, the platform provisions autonomous AI research agents orchestrated by top-tier LLMs (Groq Nodes). Upon trigger, the AI ecosystem instantly scans live global economic signals using specialized search tools (`SerperDevTool`), synthesizing complex micro-news and macro catalysts into comprehensive corporate briefings.
* **Dynamic Asset Scalability:** Transitioned from static selectors to an open ticker-targeting input model, enabling native tracking for global indices, equities, spot metals (e.g., Gold - `GC=F`), Brent Crude, and digital assets.
* **Production-Grade Architecture:** Fully modular UI wrapped inside `Streamlit`, leveraging custom CSS injections to suppress standard layout overheads, optimize device viewport layout, and deliver an enterprise-grade viewport flow.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit, Custom CSS (GitHub Dark Mode Matrix)
* **Data Science & Charting:** Pandas, Plotly (Interactive Candlesticks & Overlays)
* **Data Pipelines:** Yahoo Finance API (`yfinance`)
* **AI Infrastructure:** CrewAI Architecture, Groq Node Integration (Llama 3.3 70B), Serper Dev API

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Stock-Market-Ratio-Analysis.git](https://github.com/YOUR_USERNAME/Stock-Market-Ratio-Analysis.git)
   cd Stock-Market-Ratio-Analysis