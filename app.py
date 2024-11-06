import os
import matplotlib.pyplot as plt
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()

# Set up Streamlit
st.title("Stock News Sentiment Analysis")
st.write("This app analyzes sentiment from news headlines for selected stocks.")

# Define URL and headers for Finviz
finviz_url = 'https://finviz.com/quote.ashx?t='
headers = {'user-agent': 'my-app'}

# User input for stock tickers
tickers_input = st.text_input("Enter stock tickers separated by commas (e.g., AAPL, TSLA, AMZN):", "BSCO, GOLD, NVDA")
tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
st.write("Analyzing tickers:", ", ".join(tickers))

# Fetch and parse news tables
news_tables = {}
for ticker in tickers:
    try:
        url = finviz_url + ticker
        req = Request(url=url, headers=headers)
        response = urlopen(req)
        html = BeautifulSoup(response, features='html.parser')
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")

# Parse news headlines and perform sentiment analysis
parsed_data = []
for ticker, news_table in news_tables.items():
    if news_table:
        for row in news_table.findAll('tr'):
            title = row.a.text
            compound_score = vader.polarity_scores(title)['compound']
            parsed_data.append([ticker, title, compound_score])

# Create DataFrame from parsed data
df = pd.DataFrame(parsed_data, columns=['ticker', 'title', 'compound'])

# Display DataFrame and analysis results
if df.empty:
    st.warning("No relevant news headlines found.")
else:
    st.write("### Parsed News Headlines with Sentiment Scores")
    st.dataframe(df)

    # Calculate average compound score per ticker
    avg_compound_scores = df.groupby('ticker')['compound'].mean().reset_index()
    avg_compound_scores.columns = ['ticker', 'average_compound']
    st.write("### Average Sentiment Scores by Ticker")
    st.dataframe(avg_compound_scores)

    # Plotting the sentiment scores
    st.write("### Sentiment Analysis Bar Chart")
    plt.figure(figsize=(10, 6))
    mean_df = df.groupby('ticker')['compound'].mean()
    mean_df.plot(kind='bar', title='Sentiment Analysis of Stock News')
    plt.xlabel('Ticker')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot in Streamlit
    st.pyplot(plt)

    # Save the results to CSV files
    avg_compound_scores.to_csv('average_compound_scores.csv', index=False)
    df.to_csv('sentiment_results.csv', index=False)
    st.success("Results saved to CSV files.")

    # Provide download links for the CSV files
    st.download_button(
        label="Download Average Sentiment Scores CSV",
        data=open('average_compound_scores.csv', 'rb').read(),
        file_name='average_compound_scores.csv',
        mime='text/csv'
    )
    st.download_button(
        label="Download Sentiment Results CSV",
        data=open('sentiment_results.csv', 'rb').read(),
        file_name='sentiment_results.csv',
        mime='text/csv'
    )
