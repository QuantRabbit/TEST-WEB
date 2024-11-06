import os
import matplotlib.pyplot as plt
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

nltk.download('vader_lexicon')

# Initialize SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()

# Set up Streamlit with custom styling
st.set_page_config(page_title="Stock News Sentiment Analysis", layout="wide")
st.title("📈 Stock News Sentiment Analysis")
st.markdown("Analyze the sentiment from recent news headlines for selected stocks to gain insights into market sentiment.")

# User input for stock tickers
st.sidebar.header("Customize Your Analysis")
tickers_input = st.sidebar.text_input(
    "Enter stock tickers separated by commas (e.g., AAPL, TSLA, AMZN):", "BSCO, GOLD, NVDA"
)
tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]
st.sidebar.write("Analyzing tickers:", ", ".join(tickers))

# Button to analyze the data
analyze_button = st.sidebar.button("Analyze Data")

if analyze_button:
    # Fetch and parse news tables
    st.header("Fetching and Analyzing News...")
    news_tables = {}
    for ticker in tickers:
        try:
            url = f'https://finviz.com/quote.ashx?t={ticker}'
            req = Request(url=url, headers={'user-agent': 'my-app'})
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
    df = pd.DataFrame(parsed_data, columns=['Ticker', 'Title', 'Compound Score'])

    # Display results with improved layout
    if df.empty:
        st.warning("No relevant news headlines found. Please try different tickers.")
    else:
        # Display parsed news headlines
        st.subheader("📰 Parsed News Headlines with Sentiment Scores")
        st.dataframe(df.style.format({"Compound Score": "{:.2f}"}))

        # Calculate average compound score per ticker
        avg_compound_scores = df.groupby('Ticker')['Compound Score'].mean().reset_index()
        avg_compound_scores.columns = ['Ticker', 'Average Sentiment Score']

        # Display average sentiment scores
        st.subheader("📊 Average Sentiment Scores by Ticker")
        st.dataframe(avg_compound_scores.style.format({"Average Sentiment Score": "{:.2f}"}))

        # Plotting the sentiment scores with an improved design
        st.subheader("📈 Sentiment Analysis Bar Chart")
        fig, ax = plt.subplots(figsize=(10, 6))
        mean_df = df.groupby('Ticker')['Compound Score'].mean()
        mean_df.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Sentiment Analysis of Stock News', fontsize=14, weight='bold')
        ax.set_xlabel('Ticker', fontsize=12)
        ax.set_ylabel('Average Sentiment Score', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(visible=True, linestyle='--', alpha=0.5)
        st.pyplot(fig)

        # Save results to CSV files and provide download links
        avg_compound_scores.to_csv('average_compound_scores.csv', index=False)
        df.to_csv('sentiment_results.csv', index=False)
        
        st.success("Analysis complete! Download your results below.")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Download Average Sentiment Scores CSV",
                data=open('average_compound_scores.csv', 'rb').read(),
                file_name='average_compound_scores.csv',
                mime='text/csv'
            )
        with col2:
            st.download_button(
                label="Download Sentiment Results CSV",
                data=open('sentiment_results.csv', 'rb').read(),
                file_name='sentiment_results.csv',
                mime='text/csv'
            )

# Footer with credits
st.markdown("---")
st.markdown("**Created by QantRabbit** | 📊 Powered by Finviz and VADER Sentiment Analysis | © 2024")

