# 📈 Real-Time Market Sentiment Engine
**An End-to-End Data Pipeline for Financial Intelligence**

### 🚀 [View Live App](https://your-streamlit-link-here.streamlit.app)

## 📋 Project Overview
This project is a real-time data tool designed to quantify market "mood" during high-volatility sessions (e.g., Black Monday 2026). It scrapes live financial headlines, performs Natural Language Processing (NLP) to assign sentiment scores, and visualizes the results in an interactive dashboard.

##  Tech Stack
- **Language:** Python 3.13
- **Data Collection:** BeautifulSoup (Web Scraping)
- **NLP Engine:** VADER Sentiment Analysis
- **Visualization:** Plotly & Streamlit
- **Deployment:** GitHub & Streamlit Community Cloud

##  Key Features
- **Live Scraping:** Bypasses static datasets by fetching real-time headlines from Google News.
- **Search Filtering:** Dynamic keyword filtering (e.g., 'Nifty', 'Reliance', 'Oil') to isolate specific sector sentiment.
- **Sentiment Gauge:** An aggregated "Panic vs. Greed" meter for instant market assessment.
- **Data Portability:** Integrated CSV export feature for further analysis in Excel/SQL.

## Architecture
1. **Extract:** Scrapes raw HTML using `requests` and `BeautifulSoup`.
2. **Transform:** Processes text through `vaderSentiment` and cleans data via `Pandas`.
3. **Load:** Deploys interactive UI via `Streamlit` with a 10-minute caching layer to optimize performance.

---
