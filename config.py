# config.py

# --- Scraping Configuration ---
# Hashtags to search for on Twitter/X
HASHTAGS = ["#nifty50", "#sensex", "#intraday", "#banknifty"]

# Combine hashtags into a search query. The "OR" operator finds tweets with any of these hashtags.
# "lang:en" filters for English language tweets. " -is:retweet" excludes retweets.
# SEARCH_QUERY = f'({" OR ".join(HASHTAGS)}) lang:en -is:retweet'
SEARCH_QUERY = f'{" OR ".join(HASHTAGS)} lang:en -is:retweet'

# Target number of unique tweets to scrape
TARGET_TWEET_COUNT = 2000

# Playwright configuration
HEADLESS_MODE = False  # Set to False to watch the browser in action
SCRAPING_TIMEOUT = 120000 # Timeout in milliseconds (e.g., 120 seconds)


# --- Data Storage Configuration ---
OUTPUT_DATA_DIR = "data"
PARQUET_FILE_PATH = f"{OUTPUT_DATA_DIR}/tweets.parquet"


# --- Analysis Configuration ---
ANALYSIS_PLOT_PATH = f"{OUTPUT_DATA_DIR}/market_sentiment_analysis.png"
# TIME_SERIES_INTERVAL = "15T" # Resample sentiment data into 15-minute intervals
TIME_SERIES_INTERVAL = "15min" # Resample sentiment data into 15-minute intervals