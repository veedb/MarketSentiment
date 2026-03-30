import streamlit as st
import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import plotly.express as px

# 1. Page Config (The "Branding")
st.set_page_config(page_title="Indian Market Sentiment Tracker", layout="wide")
st.title("📊 Real-Time Indian Market Sentiment")
st.subheader("Monitoring Black Monday & Sector Crashes (March 2026)")

# 2. The Logic (The "Scraper")
@st.cache_data(ttl=600) # Only scrape every 10 mins to be "polite" to the server
def get_live_news():
    url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-IN&gl=IN&ceid=IN%3Aen"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='gPFEn')
    return [item.text for item in articles[:15]]

# 3. The Sentiment Engine
analyzer = SentimentIntensityAnalyzer()
headlines = get_live_news()

# 4. Process the data
results = []
for h in headlines:
    score = analyzer.polarity_scores(h)['compound']
    results.append({"Headline": h, "Score": score})

df = pd.DataFrame(results)

# 5. The Sidebar (The "Controls")
st.sidebar.header("Project Info")
st.sidebar.write("**Built by: Ved**")
st.sidebar.write("Tools: Python, BeautifulSoup, VADER Sentiment, Streamlit")
st.sidebar.write("This tool tracks the 'Market Mood' during volatile sessions.")

# 6. Display the Visuals (The "Dazzle")
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### Latest Sentiment Analysis")
    # Color coding the bars
    df['Status'] = df['Score'].apply(lambda x: 'Bullish' if x > 0 else ('Bearish' if x < 0 else 'Neutral'))
    fig = px.bar(df, x='Score', y='Headline', orientation='h', 
                 color='Status', color_discrete_map={'Bullish': 'green', 'Bearish': 'red', 'Neutral': 'gray'},
                 title="Market Sentiment Score (-1 to 1)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### Market Summary")
    bearish_count = len(df[df['Score'] < 0])
    bullish_count = len(df[df['Score'] > 0])
    st.metric("Bearish Headlines", bearish_count, delta="-Bad News" if bearish_count > 5 else "Normal")
    st.metric("Bullish Headlines", bullish_count, delta="Good News" if bullish_count > 5 else "Normal")

st.write("### Data Preview")
st.dataframe(df)