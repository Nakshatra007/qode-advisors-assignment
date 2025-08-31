# src/analysis.py

import logging
import pandas as pd
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config import TIME_SERIES_INTERVAL, ANALYSIS_PLOT_PATH

def perform_analysis(df):
    """
    Performs sentiment analysis and generates insights from the processed data.

    Args:
        df (pandas.DataFrame): The cleaned and processed tweet data.
    """
    if df.empty:
        logging.warning("DataFrame is empty. Skipping analysis.")
        return

    # 1. Text-to-Signal Conversion (Sentiment Analysis)
    analyzer = SentimentIntensityAnalyzer()
    df['sentiment_score'] = df['content_cleaned'].apply(
        lambda x: analyzer.polarity_scores(x)['compound']
    )
    logging.info("Sentiment analysis complete.")

    # 2. Signal Aggregation
    # Create a weighted sentiment score based on engagement
    df['weighted_sentiment'] = df['sentiment_score'] * (1 + df['engagement_likes'] + df['engagement_retweets'])
    
    # Set timestamp as index for time-series analysis
    df.set_index('timestamp', inplace=True)
    
    # Resample to create a time-series signal
    sentiment_over_time = df['sentiment_score'].resample(TIME_SERIES_INTERVAL).mean()
    logging.info(f"Aggregated sentiment signal into {TIME_SERIES_INTERVAL} intervals.")

    # 3. Memory-Efficient Visualization
    create_sentiment_plot(sentiment_over_time)

def create_sentiment_plot(sentiment_series):
    """
    Creates and saves a plot of sentiment over time.
    """
    # plt.style.use('seaborn-v0_8-grid')
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(15, 7))

    sentiment_series.plot(ax=ax, color='blue', linewidth=2, marker='o', markersize=4)

    ax.set_title('Indian Stock Market Sentiment Over Time', fontsize=16)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Average Sentiment Score', fontsize=12)
    ax.axhline(0, color='red', linestyle='--', linewidth=1, label='Neutral')
    
    plt.legend()
    plt.tight_layout()
    
    try:
        plt.savefig(ANALYSIS_PLOT_PATH)
        logging.info(f"Analysis plot saved to {ANALYSIS_PLOT_PATH}")
    except Exception as e:
        logging.error(f"Failed to save plot: {e}")



import logging
import os
import pandas as pd

from src.scraper import scrape_tweets
from src.data_processor import process_data
from src.analysis import perform_analysis
from config import PARQUET_FILE_PATH, OUTPUT_DATA_DIR

# --- Setup Logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def main():
    """
    Main function to run the end-to-end data pipeline.
    """
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DATA_DIR):
        os.makedirs(OUTPUT_DATA_DIR)
        logging.info(f"Created directory: {OUTPUT_DATA_DIR}")

    # --- 1. Data Collection ---
    logging.info("Starting Step 1: Data Collection")
    raw_tweets = scrape_tweets()
    if not raw_tweets:
        logging.error("Scraping returned no data. Exiting pipeline.")
        return

    # --- 2. Data Processing & Storage ---
    logging.info("Starting Step 2: Data Processing")
    processed_df = process_data(raw_tweets)

    if not processed_df.empty:
        try:
            processed_df.to_parquet(PARQUET_FILE_PATH, engine='pyarrow', index=False)
            logging.info(f"Data successfully saved to {PARQUET_FILE_PATH}")
        except Exception as e:
            logging.error(f"Failed to save data to Parquet file: {e}")
            return
    else:
        logging.warning("Processed DataFrame is empty. Nothing to save or analyze.")
        return

    # --- 3. Analysis & Insights ---
    logging.info("Starting Step 3: Analysis & Insights")
    # Read from the saved file to simulate a real pipeline
    df_for_analysis = pd.read_parquet(PARQUET_FILE_PATH)
    perform_analysis(df_for_analysis)
    
    logging.info("Pipeline executed successfully.")


if __name__ == "__main__":
    main()