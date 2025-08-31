# src/data_processor.py

import pandas as pd
import re
import logging
from ftfy import fix_text

def process_data(tweets_list):
    """
    Cleans, normalizes, and transforms a list of raw tweet data.

    Args:
        tweets_list (list): A list of dictionaries containing raw tweet data.

    Returns:
        pandas.DataFrame: A cleaned and processed DataFrame.
    """
    if not tweets_list:
        logging.warning("Received an empty list of tweets. Returning an empty DataFrame.")
        return pd.DataFrame()

    df = pd.DataFrame(tweets_list)

    # 1. Deduplication
    df.drop_duplicates(subset=['tweet_id'], keep='first', inplace=True)
    logging.info(f"Removed duplicates. {len(df)} unique tweets remaining.")

    # 2. Data Type Conversion and Handling Missing Values
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    for col in ['engagement_replies', 'engagement_retweets', 'engagement_likes']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # 3. Text Cleaning and Normalization
    df['content_cleaned'] = df['content'].apply(clean_tweet_text)

    # 4. Handle Unicode and special characters
    df['content_cleaned'] = df['content_cleaned'].apply(lambda x: fix_text(x))
    
    # 5. Reorder columns for clarity
    final_columns = [
        'tweet_id', 'timestamp', 'username', 'content', 'content_cleaned',
        'engagement_replies', 'engagement_retweets', 'engagement_likes',
        'hashtags', 'mentions'
    ]
    df = df[final_columns]
    
    logging.info("Data processing complete.")
    return df

def clean_tweet_text(text):
    """
    A helper function to clean the text content of a tweet.
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove user @ mentions
    text = re.sub(r'\@\w+', '', text)
    # Remove hashtags (as they are already extracted)
    text = re.sub(r'\#\w+', '', text)
    # Remove newline characters and extra whitespace
    text = text.replace('\n', ' ').strip()
    return text