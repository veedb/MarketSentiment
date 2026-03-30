import streamlit as st
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Indian Market Sentiment Tracker", layout="wide")
st.title("📊 Real-Time Indian Market Sentiment")
st.subheader("Monitoring Market Mood & Sector Trends (March 2026)")

# 2. The Logic (The "Scraper")
@st.cache_data(ttl=600) 
def get_live_news():
    url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='gPFEn')
    return [item.text for item in articles[:20]]

# 3. Data Processing & Search Filter
all_headlines = get_live_news()
search_term = st.text_input("🔍 Filter headlines by keyword (e.g., 'Nifty', 'Reliance', 'Fed')")

if search_term:
    headlines = [h for h in all_headlines if search_term.lower() in h.lower()]
else:
    headlines = all_headlines

analyzer = SentimentIntensityAnalyzer()
results = []
for h in headlines:
    score = analyzer.polarity_scores(h)['compound']
    results.append({"Headline": h, "Score": score})

df = pd.DataFrame(results)

# 4. The Sidebar
st.sidebar.header("Project Info")
st.sidebar.write(f"👤 **Developer:** Ved")
st.sidebar.write("🛠️ **Tools:** Python, VADER, Plotly, Streamlit")
now = datetime.now().strftime("%d %b %Y | %H:%M:%S")
st.sidebar.info(f"Last Data Sync: {now}")

# 5. Display the Visuals
if not df.empty:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("### Latest Sentiment Analysis")
        df['Status'] = df['Score'].apply(lambda x: 'Bullish' if x > 0 else ('Bearish' if x < 0 else 'Neutral'))
        fig = px.bar(df, x='Score', y='Headline', orientation='h', 
                     color='Status', color_discrete_map={'Bullish': 'green', 'Bearish': 'red', 'Neutral': 'gray'},
                     title="Headline Sentiment Scores")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write("### Market Summary")
        avg_score = df['Score'].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = avg_score,
            title = {'text': "Overall Mood", 'font': {'size': 18}},
            gauge = {'axis': {'range': [-1, 1]},
                     'bar': {'color': "black"},
                     'steps': [
                         {'range': [-1, -0.2], 'color': "#ff4b4b"},
                         {'range': [-0.2, 0.2], 'color': "#f0f2f6"},
                         {'range': [0.2, 1], 'color': "#238636"}]}))
        fig_gauge.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    st.write("### Data Preview")
    st.dataframe(df, use_container_width=True)

    # 6. Export Feature
    st.markdown("---")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Sentiment Data as CSV",
        data=csv,
        file_name='market_sentiment_report.csv',
        mime='text/csv'
    )
else:
    st.warning(f"No headlines found for '{search_term}'. Try a different keyword!")